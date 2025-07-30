""" In this version, I expect all point clouds to be of same length. This allows me to batch all operations,
    in particular for the SO(3) local minima search. I believe overall it provides ~ 30% speed improvement.
    Batching everything while allowing varying inputs shapes is feasible, typically through the message
    passing scheme employed in torch geometric (aka graph processing). I didn't implement that though.
"""

from __future__ import annotations
from typing import Callable, Optional, Any, cast
from functools import partial, wraps
from time import perf_counter
import torch
from torch import Tensor
from pytorch3d.transforms import Transform3d
from pytorch3d.ops.utils import eyes
# from .icp import icp
from .se3 import make_se3_sampling
from .initializers import make_initializer, MinimaInitializer, LocalMinimaInitializer
from .utils.pcd import center, pairwise_max_norm, rescale_scene, unflatten
from .utils.misc import apply_transform, batch, default_device
from .utils.chamfer import ChamferDistance, compute_integral
from .utils.types import RegistrationFn, Criterion, Device


# _________________________________________________________________________________________________________ #

def timed(method: Callable) -> Callable:
    @wraps(method)
    def wrapper(self, *args, **kwargs) -> Any:
        tic = perf_counter()
        out = method(self, *args, **kwargs)
        toc = perf_counter()
        self.elapsed_time[method.__name__] = toc - tic
        return out
    return wrapper


# _________________________________________________________________________________________________________ #

class PairwiseGRIP:

    def __init__(
        self,
        # Core
        registration_fn: RegistrationFn,
        criterion: Optional[Criterion] = None,
        # Preprocess
        center: bool = True,
        pairwise_max_norm: bool = True,
        scale: float = -1,
        # Chamfer
        bidirectional: bool = False,
        trim_ratio: float = 0.,
        # SE(3) sampling
        sampling: str = 'uniform',  # choices = ['uniform' , 'random']
        N_R: int = 512,
        N_t: int = 4,
        t_amplitude: float = 0.2,
        # Poses Initializations
        strategy: str = 'local_minima',  # ['exhaustive', 'minima', 'local_minima']
        num_init: int = -1,
        # Local Minima Search
        neighbors: int = 32,
        cache_dir: Optional[str] = '.cache',
        parallel_search: bool = True,
        # Best minimum search
        integral_test: Optional[Tensor] = None,
        # VRAM usage
        batch_size: int = 50_000,
        monitor_vram: bool = False,
        gpu_index: int = 0,
        # Logging
        verbose: bool = True,
        progress_bar: bool = False,
        device: Optional[Device] = None,
    ) -> None:
        """ Setup the GRIP algorithm for pairwise registration.

        Args:
            registration_fn (Callable):
                Base registration function upon which GRIP will be executed. It MUST have the following
                signature:
                    `T_hat: Tensor = registration_fn(sources: Tensor, models: Tensor)`
                where:
                    - `sources` and `models` are batches of point clouds `(B, N, 3)`.
                    - `T_hat_batched` is a batch of rigid motions `(B, 4, 4)`.
            criterion (Callable, optional):
                Scalar valued function to evaluate the quality of a registration. If provided, it MUST have
                the following signature:
                    `losses = criterion(registered_sources, models)`
                where:
                    - `registered_sources` and `models` are tensors of of point clouds batches `(B, N, 3)`.
                    - `T_hat_batched` is a batch of rigid motions `(B, 4, 4)`.
                If `None`, GRIP will use the Chamfer distance. Defaults to `None`.
            bidirectional (str):
                Only used when criterion is None. Direction of the Chamfer distances. If `True`, compute both
                sources to models and models to sources, otherwise compute sources to models only.
                Defaults to `False`.
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
                Number of neighbors to consider for the SO(3) local minima search. Defaults to `64`.
            J (int, optional):
                Maximal number of local minima to consider per source. Defaults to `64`.
            chunk_size (int, optional):
                Number of views being handled in parallel. Controls memory consumption. VRAM usage can be
                monitored with progress_bar=True and monitor_vram=True. Defaults to 4.
            batch_size (int, optional): Number of Chamfer distances being computed in parallel. Controls
                memory consumption. VRAM usage can be monitored with progress_bar=True and monitor_vram=True.
                Defaults to 100_000.
            parallel_search (bool, optional):
                If `True`, search local minima for all views in parallel. Linearly faster (w.r.t the number
                of point clouds), but consumes a lot more memory. Defaults to `True`.
            verbose (bool, optional):
            If `True`, display GRIP step advancements. Defaults to `True`.
            progress_bar (bool):
                If True, display progress bars for the SO(3) local minima search. Defaults to `False`.
        """
        self.device = device if device is not None else default_device()
        self.registration_fn = registration_fn
        self.center = center
        self.pairwise_max_norm = pairwise_max_norm
        self.scale = scale
        self.se3 = make_se3_sampling(sampling, N_R, N_t, t_amplitude, self.device)
        self.num_transforms = len(self.se3)
        self.trim_ratio = trim_ratio
        self.criterion = criterion if criterion is not None else ChamferDistance(bidirectional=bidirectional,
                                                                                 trim_ratio=trim_ratio)
        self.initializer = make_initializer(strategy, self.se3, self.criterion, num_init, batch_size,
                                            neighbors, parallel_search, cache_dir, verbose, progress_bar,
                                            monitor_vram, gpu_index)
        if integral_test is not None:
            self.compute_integral = partial(compute_integral,
                                            overlap_range=integral_test, bidirectional=bidirectional)
        self.batch_size = batch_size
        self.batch = partial(batch, batch_size=self.batch_size)
        self.sampling = sampling
        self.strategy = strategy
        self.verbose = verbose
        self.elapsed_time = {}

    def __str__(self) -> str:
        algo = self.registration_fn
        crit = self.criterion
        algo_name = algo.func.__name__ if isinstance(algo, partial) else algo.__name__
        if crit.__class__.__name__ == 'function':
            crit_name = crit.func.__name__ if isinstance(crit, partial) else crit.__name__  # type: ignore
        else:
            crit_name = crit.__class__.__name__
        string = (f'{self.__class__.__name__}:\n'
                  f'N={len(self.se3):,} | algo={algo_name} | criterion={crit_name}')
        return string

    def print_if_verbose(self, msg: str) -> None:
        if self.verbose:
            print(msg)

    # _____________________________________________________________________________________________________ #

    def preprocess(self, S: Tensor, M: Tensor) -> None:
        """ Center & Pairwise Max Norm. S & M: batched of point clouds (B, N_s, 3), (B, N_m, 3). """
        self.num_views = len(S)
        self.sources, self.models = S, M
        self.dtype = self.sources.dtype
        # 1. Center
        if self.center:
            self.sources, self.sources_means = center(S)
            self.models, self.models_means = center(M)
        else:
            self.sources_means = torch.zeros(len(S), 1, 3, dtype=self.dtype, device=S.device)
            self.models_means = torch.zeros(len(M), 1, 3, dtype=self.dtype, device=M.device)
        # 2. Scale
        if self.scale > 0:
            self.sources, self.models, self.scales = rescale_scene(self.sources, self.models, self.scale)
        # 3. Pairwise max norm
        elif self.pairwise_max_norm:
            self.sources, self.models, self.scales = pairwise_max_norm(self.sources, self.models)
        else:
            self.scales = torch.ones(len(self.sources), dtype=self.dtype, device=self.sources.device)

    @timed
    def initialize(self) -> None:
        """ Apply SE(3) sampling to sources, and optionally search for minima. """
        if isinstance(self.initializer, MinimaInitializer):
            msg = (f":: Selecting potential inits from {self.num_transforms:,} "
                   f"{self.sampling} motions using {self.strategy.replace('_', ' ')} strategy ...")
        else:
            msg = f":: Applying {self.num_transforms:,} motions to sources ..."
        self.print_if_verbose(msg)
        initializations = self.initializer(self.sources, self.models, self.criterion)
        self.transforms_starts, self.sources_starts, self.models_starts = initializations

    @timed
    def run_registration(self) -> None:
        """ Run local refinement registration algorithm. """
        self.print_if_verbose(f':: Running {len(self.sources_starts):,} pairwise registrations ...')
        self.M_sf2m_hat = self.registration_fn(self.sources_starts, self.models_starts)

    @timed
    def get_best_minimum(self) -> None:
        """ Get best out of K minima. """
        self.print_if_verbose(':: Retrieving best pairwise results.')
        # TODO: below could be rearranged to preallocate only losses and batch over transform AND loss
        # 1. Apply estimated motions & compute all losses
        self.sf_hat = torch.empty_like(self.sources_starts, dtype=self.dtype, device=self.device)
        self.losses = torch.empty(len(self.sources_starts), dtype=self.dtype, device=self.device)
        self.batch(apply_transform, args=(self.M_sf2m_hat, self.sources_starts), out=self.sf_hat)
        criterion = self.compute_integral if hasattr(self, 'compute_integral') else self.criterion
        self.batch(criterion, args=(self.sf_hat, self.models_starts), out=self.losses)
        # 2. Unflatten
        N = self.initializer.topk if isinstance(self.initializer, MinimaInitializer) else self.num_transforms
        sizes = (self.num_views, N)
        self.losses = unflatten(self.losses, sizes)                              # (B, N)
        M_sf2m_hat = unflatten(self.M_sf2m_hat, sizes)                           # (B, N)
        self.sf_hat = unflatten(self.sf_hat, sizes)                              # (B, N, P, 3)
        self.T_starts = unflatten(self.transforms_starts, sizes)                 # (B, N, 4, 4)
        # 3. Retrieve best minimum per pair
        self.best_losses = self.losses.min(dim=1)                                # (B,)
        # 4. From best minimum, get best estimated motion, best motion start, best registered sources
        all_views_indices = torch.arange(self.num_views)
        M_sf2m_hat = M_sf2m_hat[all_views_indices, self.best_losses.indices]     # (B, 4, 4)
        M_f = self.T_starts[all_views_indices, self.best_losses.indices]         # (B, 3, 3)
        self.sources = self.sf_hat[all_views_indices, self.best_losses.indices]  # (B, P, 3)
        self.T_sf2m_hat = Transform3d(matrix=M_sf2m_hat)
        self.T_f = Transform3d(matrix=M_f)

    def compose_motions(self) -> None:
        """ Compose init and local refinement motion. """
        self.T_s2m_hat = self.T_f.compose(self.T_sf2m_hat)
        self.M_s2m_hat = self.T_s2m_hat.get_matrix()

    def run_pairwise(self) -> None:
        self.initialize()
        self.run_registration()
        self.get_best_minimum()
        self.compose_motions()

    def run_pairwise_iterated(self, S: Tensor, M: Tensor, iter: int, initial_icp_trim: float) -> Tensor:
        """ Pairwise GRIP algorithm: registrate sources onto models.

        Args:
            S (Tensor): Batch of source point clouds of same sizes: (B, N_s, 3).
            M (Tensor): Batch of model point clouds of same sizes: (B, N_m, 3).
        """
        self.preprocess(S, M)  # center & normalize once and for all
        # Initial translation only icp
        T_s2m_hat_iterated = Transform3d(matrix=eyes(4, len(S), device=S.device))
        for i in range(iter):
            if iter > 1:
                self.print_if_verbose(f':: Iter {i+1}/{iter}')
            # if i == 0:
            #     if initial_icp_trim == 0 and isinstance(self.criterion, ChamferDistance):
            #         initial_icp_trim = self.criterion.trim_ratio
            #     t_coarse = icp(self.sources, self.models,
            #                    trim_ratio=initial_icp_trim, estimate_rotation=False)[:, 3, :3]
            #     T_t_coarse = Transform3d(device=self.device).translate(t_coarse)
            #     self.sources = T_t_coarse.transform_points(self.sources)
            #     T_s2m_hat_iterated = T_s2m_hat_iterated.compose(T_t_coarse)
            self.run_pairwise()
            T_s2m_hat_iterated = T_s2m_hat_iterated.compose(self.T_s2m_hat)
        self.T_s2m_hat = T_s2m_hat_iterated
        self.M_s2m_hat = self.T_s2m_hat.get_matrix()
        self.M_s2m_hat[:, 3, :3] = self.reframe_translations().squeeze(dim=1)
        return self.M_s2m_hat

    def reframe_translations(self, t_hat: Optional[Tensor] = None) -> Tensor:
        """ If objets were centered and / or rescaled, the estimated translations do not
            align the original objects. This function adjusts the translation to do so.
        """
        if t_hat is None:
            t_hat = self.M_s2m_hat[:, 3, :3].clone()
        R_hat = self.M_s2m_hat[:, :3, :3]
        centroid_s = self.sources_means
        centroid_m = self.models_means
        return t_hat / self.scales[:, None] + centroid_m - centroid_s.bmm(R_hat)  # right hand convention !

    def register(
        self,
        S: Optional[Tensor] = None, M: Optional[Tensor] = None,
        iter: int = 1, initial_icp_trim: float = 0
    ) -> tuple[Tensor, Tensor]:
        motions_estimated = hasattr(self, 'M_s2m_hat')
        if motions_estimated:
            return self.sources, self.models
        if not motions_estimated and (S is None or M is None):
            missing_data_string = 'sources' if S is None else 'models'
            raise ValueError((f"You didn't provide {missing_data_string} but no motions have been "
                              "estimated yet. You most likely forgot to run estimation first."))
        S, M = cast(Tensor, S), cast(Tensor, M)
        self.run_pairwise_iterated(S, M, iter, initial_icp_trim)
        return self.sources, self.models

    def __call__(self, S: Tensor, M: Tensor, iter: int = 1, initial_icp_trim: float = 0) -> Tensor:
        """ This function returns the estimated transform. Call self.register() to get a tuple of aligned
            sources and models.
            Once finished, runtimes can be accessed through the self.elapsed_time dictionary.
        """
        return self.run_pairwise_iterated(S, M, iter, initial_icp_trim)

    @property
    def config(self) -> dict:
        num_init = self.initializer.topk if hasattr(self.initializer, 'topk') else self.num_transforms
        if hasattr(self.initializer, 'knn_graph'):
            self.initializer = cast(LocalMinimaInitializer, self.initializer)
            neighbors = self.initializer.knn_graph.K
        else:
            neighbors = None
        # ! Currently don't take into account custom criterion with trim_ratio or bidirectional attributes.
        if not isinstance(self.criterion, ChamferDistance):
            trim_ratio = None
            bidirectional = None
        else:
            bidirectional = self.criterion.bidirectional
            trim_ratio = self.criterion.trim_ratio
            if isinstance(self.criterion.trim_ratio, Tensor):
                trim_ratio = trim_ratio
        return {
            'center': self.center,
            'pairwise_max_norm': self.pairwise_max_norm,
            'bidirectional': bidirectional,
            'trim_ratio': trim_ratio,
            'sampling': self.sampling,
            'N_R': self.se3.N_R,
            'N_t': self.se3.N_t,
            't_amplitude': self.se3.t_amplitude,
            'strategy': self.strategy,
            'num_init': num_init,
            'neighbors': neighbors,
        }
