from __future__ import annotations
from typing import Optional
from functools import partial
from copy import deepcopy
from tqdm.auto import tqdm

import torch
from torch import Tensor

from .se3 import SE3Sampling, SE3SamplingKnnGraph
from .utils.misc import batch, apply_transform
from .utils.pcd import flatten, unflatten, expand
from .utils.types import Criterion


# _________________________________________________________________________________________________________ #

class CriterionBasedInitializer:

    """ Given any sampling of SE(3), apply it to the sources, compute losses, then, select plausible poses.
    """

    def __init__(
        self,
        se3: SE3Sampling,
        criterion: Criterion,
        batch_size: int,
        progress_bar: bool,
        monitor_vram: bool,
        gpu_index: int
    ) -> None:
        self.se3 = se3
        self.num_transforms = len(self.se3)
        self.criterion = criterion
        self.batch_size = batch_size
        self.batch = partial(batch,
                             batch_size=self.batch_size,
                             monitor_vram=monitor_vram,
                             gpu_index=gpu_index)
        self.progress_bar = progress_bar
        self.index: Tensor = torch.empty(1)
        self.topk: int = -1

    @property
    def results(self) -> tuple[Tensor, Tensor, Tensor] | Tensor:
        return (self.transforms, self.sources, self.models) if self.pairwise else self.transforms

    def transform_and_compute_losses(self, sources: Tensor, models: Tensor, transforms: Tensor) -> Tensor:
        return self.criterion(apply_transform(transforms, sources), models)

    def compute_losses_pairwise(self) -> None:
        """ Compute criterion between each source in each orientation from SE(3) sampling (V * T pointclouds)
            and each models (V pointclouds).
        """
        sources = flatten(expand(self.X, self.num_transforms, dim=1))              # (V * T, N, 3)
        models = flatten(expand(self.Y, self.num_transforms, dim=1))               # (V * T, M, 3)
        desc = 'Computing losses'
        self.losses = torch.empty(self.num_views * self.num_transforms,
                                  dtype=sources.dtype, device=self.device)
        self.batch(self.transform_and_compute_losses,
                   args=(sources, models, self.transforms), out=self.losses,
                   desc=desc, progress_bar=self.progress_bar)
        self.losses = unflatten(self.losses, (self.num_views, self.num_transforms))  # (V, T)

    def compute_losses_multiviews(self) -> None:
        """ Compute criterion between each source in each orientation from SE(3) sampling (V * T pointclouds)
            and each models (V pointclouds).
        """
        # desc = 'Computing losses'
        self.losses = torch.empty(self.num_views, self.num_transforms,
                                  dtype=self.X.dtype, device=self.device)
        iterable = tqdm(self.X, desc='Computing losses') if self.progress_bar else self.X
        for i, s in enumerate(iterable):
            losses = torch.empty(self.num_transforms, dtype=s.dtype, device=self.device)
            self.batch(self.transform_and_compute_losses,
                       args=(s, self.Y, self.transforms), out=losses, progress_bar=False)
            self.losses[i] = losses
        # self.losses = unflatten(self.losses, (self.num_views, self.num_transforms))  # (V, T)

    def prepare(self, X: Tensor, Y: Tensor) -> None:
        # V: num views, T: num transforms, P: num points (can be different for X and Y)
        self.X = X
        self.Y = Y
        self.num_views = len(self.X)
        self.num_points = self.X.shape[1]
        self.transforms = flatten(expand(self.se3.matrix, self.num_views, dim=0))  # (V * T, 4, 4)
        self.pairwise = self.Y.ndim == 3
        self.device = self.X.device

    def select(self) -> None:
        """ Provides an index (V, K) of K inits per view. """
        raise NotImplementedError

    def gather(self, data: Tensor) -> Tensor:
        return data.gather(dim=1, index=self.index[:, :, None, None].expand(-1, -1, *data.shape[-2:]))

    # def unflatten_and_gather(self, data: Tensor) -> Tensor:
    #     # (V * T, ...) -[unflatten]> (V, T, ...) -> -[gather]-> (V, K, ...) -[flatten]> (V * K, ...)
    #     return self.gather(unflatten(data, (self.num_views, self.num_transforms)))

    def reduce(self) -> None:
        # 1. prepare
        self.models = flatten(expand(self.Y, self.topk, dim=1)) if self.pairwise else self.Y
        sources = flatten(expand(self.X, self.topk, dim=1))  # (V * K, N, 3)
        # 2. Apply selected motions to sources
        # (V * T, ...) -[unflatten]> (V, T, ...) -> -[gather]-> (V, K, ...)
        self.transforms = self.gather(unflatten(self.transforms, (self.num_views, self.num_transforms)))
        if self.pairwise:  # Too VRAM costly for multiviews
            self.sources = torch.empty(self.num_views * self.topk, self.num_points, 3,
                                       dtype=sources.dtype, device=self.device)
            self.transforms = flatten(self.transforms)
            self.batch(apply_transform, args=(self.transforms, sources), out=self.sources)

    def __call__(
        self, X: Tensor, Y: Tensor, criterion: Optional[Criterion] = None
    ) -> tuple[Tensor, Tensor, Tensor] | Tensor:
        if hasattr(self, 'criterion') and criterion is not None:
            self.criterion, self.__old_criterion = criterion, deepcopy(self.criterion)
        self.prepare(X, Y)
        self.compute_losses_pairwise() if self.pairwise else self.compute_losses_multiviews()
        self.select()
        self.reduce()
        if hasattr(self, 'criterion') and criterion is not None:
            self.criterion = self.__old_criterion
        return self.results


class MinimaInitializer(CriterionBasedInitializer):

    """ Criterion based initializer (i.e. one loss per motion in given SE(3) sampling).
        Select the K motions of lowest loss.
    """

    def __init__(
        self,
        se3: SE3Sampling,
        criterion: Criterion,
        topk: int,
        batch_size: int,
        progress_bar: bool,
        monitor_vram: bool,
        gpu_index: int
    ) -> None:
        self.se3 = se3
        self.criterion = criterion
        self.num_transforms = len(self.se3)
        self.requested_topk = len(self.se3) if topk < 0 else int(topk)
        self.batch_size = batch_size
        self.batch = partial(batch,
                             batch_size=self.batch_size,
                             monitor_vram=monitor_vram,
                             gpu_index=gpu_index)
        self.progress_bar = progress_bar

    def select(self) -> None:
        self.topk = min(self.requested_topk, self.losses.shape[1])
        self.index = self.losses.topk(self.topk, dim=1, largest=False).indices  # (V, T)


# _________________________________________________________________________________________________________ #

class LocalMinimaInitializer(MinimaInitializer):

    def __init__(
        self,
        knn_graph: SE3SamplingKnnGraph,
        criterion: Criterion,
        topk: int,
        parallel_search: bool,
        batch_size: int,
        progress_bar: bool,
        monitor_vram: bool,
        gpu_index: int
    ) -> None:
        self.knn_graph = knn_graph
        self.se3 = self.knn_graph.se3
        self.num_transforms = len(self.knn_graph.se3)
        self.criterion = criterion
        self.requested_topk = None if topk < 0 else int(topk)
        self.parallel_search = parallel_search
        self.batch_size = batch_size
        self.batch = partial(batch,
                             batch_size=self.batch_size,
                             monitor_vram=monitor_vram,
                             gpu_index=gpu_index)
        self.progress_bar = progress_bar
        self.local_minima_search = partial(self.knn_graph.local_minima_search,
                                           multiviews=True,
                                           parallel=self.parallel_search)

    def select(self) -> None:
        """ Local minima search for each source. Give (V, J) potential inits. """
        minima = []
        for l in self.losses.split(self.batch_size):
            minima.extend(self.local_minima_search(l, self.requested_topk))
        self.topk = max([len(x) for x in minima]) if self.requested_topk is None else self.requested_topk
        # 3. Repeat if required and stack minima
        indices = []
        for l in minima:
            k = len(l)
            if k < self.topk:  # repeat first minimum if not enough minima, so that I can stack
                n = self.topk - k
                best_minimum = torch.as_tensor(l[0])
                l = torch.hstack((best_minimum.expand(n), torch.as_tensor(l)))
            indices.append(l)
        self.index = torch.stack(indices)


class MixedMinimaInitializer(LocalMinimaInitializer):

    def select(self) -> None:
        requested_topk = self.requested_topk
        self.requested_topk = None
        super().select()
        self.local_minima_index = self.index.clone()
        if requested_topk is None:
            raise ValueError('Topk cannot be None or negative with mixed strategy.')
        self.topk = min(requested_topk, self.losses.shape[1])
        missing = self.topk - self.local_minima_index.shape[1]
        all_minima = []
        for l, i in zip(self.losses, self.local_minima_index):
            sorted_idx = torch.argsort(l)
            i_set = set(i.tolist())
            new_idx = [idx.item() for idx in sorted_idx if idx.item() not in i_set][:missing]
            final_idx = torch.cat([i, torch.tensor(new_idx, device=self.device, dtype=torch.long)])
            all_minima.append(final_idx)
        self.index = torch.stack(all_minima)
        self.requested_topk = requested_topk


def make_initializer(
    strategy: str,  # ['absolute', 'local', 'mixed']
    se3: SE3Sampling,
    criterion: Criterion,
    num_minima: int,
    batch_size: int,
    # flames
    neighbors: int,
    parallel_search: bool,
    cache_dir: Optional[str],
    # logging
    verbose: bool,
    progress_bar: bool,
    monitor_vram: bool,
    gpu_index: int,
) -> MinimaInitializer | LocalMinimaInitializer | MixedMinimaInitializer:
    vram = (progress_bar, monitor_vram, gpu_index)
    if strategy == 'absolute':
        return MinimaInitializer(se3, criterion, num_minima, batch_size, *vram)
    # local minima
    se3_sampling_knn_graph = SE3SamplingKnnGraph(se3, neighbors, batch_size, cache_dir, verbose, *vram)
    Initializer = MixedMinimaInitializer if strategy == 'mixed' else LocalMinimaInitializer
    return Initializer(se3_sampling_knn_graph,
                       criterion, num_minima, parallel_search, batch_size, *vram)
