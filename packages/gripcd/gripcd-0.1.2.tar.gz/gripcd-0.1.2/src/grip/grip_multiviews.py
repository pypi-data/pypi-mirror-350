# pyright: reportUnboundVariable=false
from __future__ import annotations

from abc import ABC, abstractmethod
from functools import partial
from time import perf_counter
from typing import Any, Callable, Optional, cast

import torch
from pytorch3d.transforms import Transform3d
from torch import Tensor
from tqdm.auto import tqdm

from .grip_pairwise import PairwiseGRIP, Device
from .se3 import make_se3_sampling, so3_relative_angle, pairwise_rotation_errors
from .utils.chamfer import chamfer_distances_between_views_and_model
from .initializers import make_initializer
from .utils.pcd import center, max_norm
from .utils.misc import batch, apply_transform


# _________________________________________________________________________________________________________ #

def timed(method: Callable) -> Callable:
    def wrapper(self, *args, **kwargs) -> Any:
        tic = perf_counter()
        out = method(self, *args, **kwargs)
        toc = perf_counter()
        if method.__name__ in self.elapsed_time:
            self.elapsed_time[method.__name__].append(toc - tic)
        else:
            self.elapsed_time[method.__name__] = [toc - tic]
        return out
    return wrapper


# _________________________________________________________________________________________________________ #

class GenerativeMultiviewsMethod(ABC):

    """ Abstract class that generative multiviews registration methods must implement in order to be used
        with GRIP.
    """

    model: Tensor

    @abstractmethod
    def criterion(self, views: Tensor, model: Tensor | None = None) -> Tensor:
        raise NotImplementedError

    @abstractmethod
    def optimize(self, views: Tensor, generative: bool = False) -> Tensor:
        raise NotImplementedError


# _________________________________________________________________________________________________________ #

class GenerativeMultiviewsGRIP(PairwiseGRIP):

    def __init__(
        self,
        # Core
        base_method: GenerativeMultiviewsMethod,
        fix_model: bool = False,
        # Preprocessing
        center: bool = True,
        scale: bool = True,
        # Chamfer
        from_model: bool = False,
        bidirectional: bool = True,
        trim_ratio: float = 0.,
        # Optim
        R_eps: int | float = 5,
        max_iter: int = 10,
        # SE(3) sampling
        sampling: str = 'uniform',  # choices = ['uniform' , 'random']
        N_R: int = 512,
        N_t: int = 4,
        t_amplitude: float = 0.2,
        # Poses Initializations
        strategy: str = 'local_minima',  # ['minima', 'local_minima']
        num_init: int = -1,
        # Local Minima Search
        neighbors: int = 32,
        cache_dir: Optional[str] = '.cache',
        parallel_search: bool = True,
        # VRAM usage
        batch_size: int = 50_000,
        monitor_vram: bool = False,
        gpu_index: int = 0,
        # Logging
        verbose: bool = True,
        progress_bar: bool = False,
        device: Optional[Device] = None,
    ) -> None:
        """ Setup the GRIP algorithm for generative multiviews registration.

        Args:
            base_method (GenerativeMultiviewsMethod):
                Generative multiviews registration method upon which GRIP will be based. Must inherit from
                `GenerativeMultiviewsMethod`.
            from_model (bool, optional):
                Chamfer distances direction for initialization. Defaults to `False`.
            bidirectional (bool, optional):
                Chamfer distances direction for initialization. If `True`, compute both sources to model and
                model to sources, otherwise compute sources to models only. Defaults to `False`.
                Defaults to `True`.
            R_eps (int | float, optional):
                Relative angle threshold (in degree) between old and new rotations to detect escapes from
                local minima. Defaults to `30`.
            max_iter (int, optional):
                Maximal number of iterations of joint generative optimization and non generative pairwise
                restarts. Defaults to `10`.
            trim_ratio (float, optional):
                Trimming ratio of the initial Chamfer distances. Defaults to `0`.
            N_R (int, optional):
                Number of rotations uniformly sampled in SO(3). Defaults to `1_000`.
            N_t (int, optional):
                Number of translations uniformly sampled for each rotation. Defaults to `10`.
            t_amp (int, optional):
                Amplitude of the sampled translations. N_t translations will be created, along sampled
                rotations axes, with a magnitude linearly spaced from -t_amp to +t_amp. Defaults to `1_000`.
            K (int, optional):
                Number of neighbors to consider for the SO(3) local minima search. Defaults to `256`.
            J (int, optional):
                Maximal number of local minima to consider per source. Defaults to `16`.
            chunk_size (int, optional):
                Number of views being handled in parallel. Controls memory consumption. VRAM usage can be
                monitored with `progress_bar=True` and `monitor_vram=True`. Defaults to `4`.
            batch_size (int, optional): Number of Chamfer distances being computed in parallel. Controls
                memory consumption. VRAM usage can be monitored with `progress_bar=True` and
                `monitor_vram=True`. Defaults to `100_000`.
            parallel_search (bool, optional):
                If `True`, search local minima for all views in parallel. Linearly faster (w.r.t the number
                of point clouds), but consumes a lot more memory. Defaults to `True`.
            verbose (bool, optional):
                If `True`, display GRIP step advancements. Defaults to `True`.
            progress_bar (bool):
                If True, display progress bars for the SO(3) local minima search. Defaults to `False`.
            monitor_vram (bool, optional):
                If progress_bar is True, will display the current VRAM usage of the GPU (specified by
                `gpu_index`). Defaults to `False`.
            gpu_index (int, optional):
                Index of the GPU to monitor. Defaults to `0`.
        """
        if device is not None:
            self.device = device
        else:
            self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        self.base_method = base_method
        self.fix_model = fix_model
        self.center = center
        self.scale = scale
        self.from_model = from_model
        self.R_eps = R_eps
        self.max_iter = max_iter
        self.verbose = verbose
        self.progress_bar = progress_bar
        self.batch_size = batch_size
        self.se3 = make_se3_sampling(sampling, N_R, N_t, t_amplitude, self.device)
        self.num_transforms = len(self.se3)
        self.chamfer_distances = partial(chamfer_distances_between_views_and_model,
                                         from_model=from_model,
                                         bidirectional=bidirectional,
                                         trim_ratio=trim_ratio)
        self.initializer = make_initializer(strategy, self.se3, self.chamfer_distances, num_init, batch_size,
                                            neighbors, parallel_search, cache_dir, verbose, progress_bar,
                                            monitor_vram, gpu_index)
        self.batch_size = batch_size
        self.batch = partial(batch, batch_size=self.batch_size)
        self.elapsed_time = {}

    @property
    def R_hat(self) -> Tensor:
        return self.T_hat.get_matrix()[:, :3, :3]

    @timed
    def initialize(self, views: Tensor, model: Optional[Tensor] = None) -> None:
        """ If no model is provided, views[0] is considered as the model and views[1:] as the views.
            Chamfer distances between model and views, followed by flames, and best minimum (per view)
            retrieval.
        """
        self.print_if_verbose(':: Running top 1 SE(3) local minima search with Chamfer criterion')
        # 1. Initial setup
        generative = model is None
        self.original_views = views
        if self.center:
            self.original_views, self.centers = center(self.original_views)
        if self.scale:
            self.original_views, self.scales = max_norm(self.original_views)
        # self.original_views = max_norm(center(views))
        if generative:
            model, sources = self.original_views[0], self.original_views[1:]
        else:
            sources = self.original_views
        # 2. FLAMES best minimum
        # sources: (B, P_S, 3) ; model: (P_M, 3)
        self.print_if_verbose(':: Applying SE(3) sampling to sources ...')
        transforms = self.initializer(sources, model)
        transforms = cast(Tensor, transforms)
        best_transforms = transforms[:, 0, :, :]
        sources_starts = apply_transform(best_transforms, sources)
        if generative:
            V_flames_init = torch.stack((model, *sources_starts)).clone()
            M_flames_init = torch.vstack((torch.eye(4, device=model.device)[None], best_transforms))
        else:
            V_flames_init = sources_starts
            M_flames_init = best_transforms
        T_hat = Transform3d(matrix=M_flames_init).inverse().clone()
        self.base_method.model = model
        self.views, self.T_hat = V_flames_init, T_hat

    def update_estimation(self, new_T: Transform3d) -> None:
        """ Compose newly estimated motions with current estimations. """
        self.T_hat = new_T.inverse().compose(self.T_hat)
        self.views = self.T_hat.inverse().transform_points(self.original_views)

    @timed
    def joint_generative_optimization(self) -> None:
        """ Apply the base generative multiviews method and center the obtained model. """
        self.print_if_verbose(':: Running joint generative optimization')
        T_hat = self.base_method.optimize(self.views, generative=not self.fix_model)
        center = self.base_method.model.mean(dim=0)[None]  # (1, 3)
        self.base_method.model -= center
        self.print_if_verbose(f'    model length: {len(self.base_method.model)}')
        self.update_estimation(Transform3d(matrix=T_hat).translate(-center))

    @timed
    def pairwise_non_generative_restarts(self) -> None:
        """ Apply the base method in a non generative setup: for each of the N views, compute the J best
            local minima between the view and the current model estimation, and run N * J non generative
            pairwise registrations.
        """
        self.print_if_verbose(':: Running pairwise non-generative restarts')
        motion_starts = self.initializer(self.views, self.base_method.model,
                                         criterion=self.base_method.criterion)  # (V, J, 4, 4)
        motion_starts = cast(Tensor, motion_starts)
        self.print_if_verbose(f':: Found {motion_starts.shape[1]} potential inits')
        M_hat_pairwise_restart = []
        iterable = zip(tqdm(motion_starts) if self.progress_bar else motion_starts, self.views)
        for M, V in iterable:
            # J starts for i-th view
            view_starts = apply_transform(M, V)  # (J, 4, 4)
            T_hats = self.base_method.optimize(view_starts, generative=False)  # (J, 4, 4)
            views_hat = apply_transform(T_hats, view_starts)  # (J, N, 3)
            losses = self.base_method.criterion(views=views_hat)
            idx_best_local_minimum = losses.argmin()
            T_hat_pairwise_restart_i = Transform3d(matrix=M).compose(Transform3d(matrix=T_hats))
            M_hat_pairwise_restart_i = T_hat_pairwise_restart_i.get_matrix()[idx_best_local_minimum]
            M_hat_pairwise_restart.append(M_hat_pairwise_restart_i)
        T_hat_pairwise_restart = Transform3d(matrix=torch.stack(M_hat_pairwise_restart))
        self.update_estimation(T_hat_pairwise_restart)

    @timed
    def iterative_optimization(
        self, views: Tensor, model: Optional[Tensor] = None, T_gt: Tensor | None = None
    ) -> None:
        """ Initialize with best SE(3) minimum from Chamfer distances between views[0] and views[1:].
            Then, iterate join generative optimization and non generative pairwise restart until no
            new poses of best losses are found.
            If `T_gt` is provided, log the rotation error after each step.
        """
        if T_gt is not None:
            R_gt = T_gt[:, :3, :3].to(views.device)
            self.errors = {'pairwise_restarts': [], 'joint_generative': []}
        self.initialize(views, model)
        if T_gt is not None:
            self.errors['init'] = pairwise_rotation_errors(R_gt, self.R_hat)  # type: ignore
        self.joint_generative_optimization()
        if T_gt is not None:
            self.errors['joint_generative'].append(pairwise_rotation_errors(R_gt, self.R_hat))
        old_T_hat = self.T_hat.clone()
        old_losses = self.base_method.criterion(views=self.views)
        converged = False
        iter = 1
        while not converged and iter <= self.max_iter:
            self.pairwise_non_generative_restarts()
            if T_gt is not None:
                self.errors['pairwise_restarts'].append(pairwise_rotation_errors(R_gt, self.R_hat))
            self.joint_generative_optimization()
            if T_gt is not None:
                self.errors['joint_generative'].append(pairwise_rotation_errors(R_gt, self.R_hat))
            losses = self.base_method.criterion(views=self.views)
            loss_improvements = losses <= old_losses
            old_T_hat_matrix = old_T_hat.get_matrix()
            old_R_hat = old_T_hat_matrix[:, :3, :3]
            so3_distances = so3_relative_angle(self.R_hat, old_R_hat) * 180 / torch.pi
            new_poses = so3_distances >= self.R_eps
            local_minima_escapes = torch.logical_and(loss_improvements, new_poses).sum().item()
            converged = local_minima_escapes == 0
            self.print_if_verbose((
                f'Iter n°{iter}: loss improvements={loss_improvements.sum().item()} | '
                f'New poses={new_poses.sum().item()} | Local Minima Escape={local_minima_escapes}'
            ))
            if converged:
                self.print_if_verbose((f':: GRIP({self.base_method.__class__.__name__}) '
                                       f'converged in {iter+1} iterations.'))
                break
            # 4. Replace by new T where loss improvements
            T_hat_matrix = self.T_hat.get_matrix()
            old_T_hat_matrix[loss_improvements] = T_hat_matrix[loss_improvements]
            self.T_hat = Transform3d(matrix=old_T_hat_matrix)
            old_losses = losses.clone()
            old_T_hat = self.T_hat.clone()
            iter += 1
        if T_gt is not None:
            self.errors['final'] = pairwise_rotation_errors(R_gt, self.R_hat)  # type: ignore

    def __call__(  # type: ignore
        self, views: Tensor, model: Optional[Tensor] = None, T_gt: Optional[Tensor] = None
    ) -> None:
        """ Once finished, runtimes can be accessed through the self.elapsed_time dictionary. """
        self.iterative_optimization(views, model, T_gt)
