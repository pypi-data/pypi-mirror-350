from __future__ import annotations
from typing import Optional, cast
from pathlib import Path
from tqdm.auto import tqdm
import nvidia_smi  # nvidia-ml-py3

import torch
from torch import Tensor
from pytorch3d.transforms import Transform3d, quaternion_to_matrix, random_rotations
from .utils import flatten, expand
from .utils.types import Device, SE3KnnGraph
from .utils.misc import default_device, bytes2human


# +-------------------------------------------------------------------------------------------------------+ #
# |                                            SE(3) DISTANCES                                            | #
# +-------------------------------------------------------------------------------------------------------+ #

def so3_relative_angle(R1: Tensor, R2: Tensor) -> Tensor:
    """ SO(3) geodesic distance between two batches of rotation matrices. """
    cos_theta = (torch.vmap(torch.trace)(R1 @ R2.mT) - 1) / 2
    cos_theta = torch.clamp(cos_theta, -1, 1)
    return torch.acos(cos_theta)


def pairwise_rotation_errors(R_gt: Tensor, R_hat: Tensor) -> Tensor:
    """ If N rotations have been estimated to align N views in an arbitrary orientation, and we need to
        compute the estimation error, we have to compute the pairwise SO(3) geodesic distance between
        R_hat[i]R_gt[i] and R_hat[j]R_gt[j], resulting in N(N-1)/2 distances. This function computes
        these N(N-1)/2 distances in parallel.
    Args:
        R_gt (Tensor): Groundtruth poses (N, 3, 3).
        R_hat (Tensor): Estimated poses (N, 3, 3).

    Returns:
        Tensor: Pairwise rotation estimation error (N(N-1)/2,).
    """
    assert len(R_gt) == len(R_hat)
    N = len(R_gt)
    I, J = torch.triu_indices(N, N, offset=1)
    Ri = R_hat[I] @ R_gt[I]
    Rj = R_hat[J] @ R_gt[J]
    return so3_relative_angle(Ri, Rj)


def se3_geodesic_distance(
    T1: Tensor,
    T2: Tensor,
    t_weight: float | Tensor = 1,
    return_both: bool = False
) -> Tensor | tuple[Tensor, Tensor]:
    zero = torch.tensor(0, dtype=T1.dtype, device=T1.device)
    if not T1[:, :3, 3].allclose(zero):
        print('[WARNING] Are you sure T1 is in right-hand convention ?')
    if not T2[:, :3, 3].allclose(zero):
        print('[WARNING] Are you sure T2 is in right-hand convention ?')
    R_1, t_1 = T1[:, :3, :3], T1[:, 3, :3]  # /!\ WARNING: right hand motion in PyTorch3D !
    R_2, t_2 = T2[:, :3, :3], T2[:, 3, :3]  # /!\ WARNING: right hand motion in PyTorch3D !
    dist_R_square = so3_relative_angle(R_1, R_2) ** 2
    dist_t_square = t_weight * torch.linalg.vector_norm(t_1 - t_2, dim=1) ** 2
    if return_both:
        return dist_R_square, dist_t_square
    return (0.5 * dist_R_square + 0.5 * dist_t_square).sqrt()


def batched_k_min_pairwise_se3_geodesic_distances(
    T1: Tensor,
    T2: Tensor,
    t_weight: float | Tensor,
    neighbors: int,
    batch_size: int,
    progress_bar: bool,
    device: Device,
    monitor_vram: bool,
    gpu_index: int,
) -> tuple[Tensor, Tensor]:
    """ Slow but less memory. """
    N = len(T1)
    iterations = tqdm(range(N), desc='Computing pairwise distances') if progress_bar else range(N)
    k_min_distances = torch.empty(N, neighbors, dtype=T1.dtype, device=device)
    k_min_indices = torch.empty(N, neighbors, dtype=T1.dtype, device=device)
    if monitor_vram and progress_bar:
        nvidia_smi.nvmlInit()
        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(gpu_index)
    for i in iterations:
        distances = []
        for j_start in range(0, N, batch_size):  # Batch on j only
            j_end = min(j_start + batch_size, N)
            d = se3_geodesic_distance(expand(T1[i], j_end - j_start, 0), T2[j_start:j_end], t_weight)
            distances.append(d)
        distances = torch.hstack(distances)  # 1D tensor of length N
        min_k = distances.topk(neighbors + 1, largest=False)  # exclude itself
        k_min_distances[i] = min_k.values[1:]                 # exclude itself
        k_min_indices[i] = min_k.indices[1:]                  # exclude itself
        if progress_bar and monitor_vram:
            gpu_info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)  # type: ignore
            iterations.set_postfix_str(f'VRAM: {bytes2human(gpu_info.used)}')  # type: ignore
    return k_min_distances, k_min_indices


# +-------------------------------------------------------------------------------------------------------+ #
# |                                            SE(3) SAMPLING                                             | #
# +-------------------------------------------------------------------------------------------------------+ #

def super_fibonacci_spirals(n: int, device: Device) -> Tensor:
    """ Generate n samples on SO(3) as unit quaternions, then convert them to Euler's angles.
    Alexa M., Super-Fibonacci Spirals: Fast, Low-Discrepancy Sampling of SO3, CVPR 2022.
    """
    phi = torch.sqrt(torch.as_tensor(2.0, dtype=torch.float32))
    psi = 1.533751168755204288118041  # solution of ψ^4 = ψ + 4, decimal expansion sufficient for float64
    Q = torch.empty(size=(n, 4), dtype=torch.float32, device=device)
    i = torch.arange(n, device=device)
    s = (i + 0.5).float()
    r = torch.sqrt(s / n).float()
    R = torch.sqrt(1.0 - s / n)
    alpha = 2.0 * torch.pi * s / phi
    beta = 2.0 * torch.pi * s / psi
    Q[i, 0] = r * torch.sin(alpha)
    Q[i, 1] = r * torch.cos(alpha)
    Q[i, 2] = R * torch.sin(beta)
    Q[i, 3] = R * torch.cos(beta)
    matrices = quaternion_to_matrix(Q)
    return matrices


def N_t_from_N_R(N_R: int, alpha: float, device: Optional[Device] = None) -> int:
    """ Guess a good N_t from a given N_R. """
    device = device if device is not None else default_device()
    # 1. Compute pairwise rotation distances
    R = super_fibonacci_spirals(N_R, device)
    d_R = torch.empty(N_R, N_R, dtype=R.dtype, device=device)
    I, J = torch.triu_indices(N_R, N_R, 1)
    d_R[I, J] = d_R[J, I] = so3_relative_angle(R[I], R[J])
    d_R = d_R.flatten()[1:].view(N_R - 1, N_R + 1)[:, :-1].reshape(N_R, N_R - 1)  # remove diagonal
    # 2. Get average distance to nearest neighbors
    mean_delta_R = d_R.min(dim=1).values.mean()
    # 3. Deduce delta_t norm, then N_t
    delta_t = mean_delta_R / alpha
    N_t = round(1 + 2 / delta_t.item())
    print(f'{N_R=} -> mean_delta_R={mean_delta_R.item():.2f} -> {N_t=}')
    return N_t


def sample_translations_grid(N_t: int, t_amplitude: float, device: Device) -> Tensor:
    grid_linspace = torch.linspace(-t_amplitude, t_amplitude, N_t, device=device)
    gx, gy, gz = torch.meshgrid(grid_linspace, grid_linspace, grid_linspace, indexing='ij')
    translations = torch.stack((gx, gy, gz), dim=-1).reshape(-1, 3)  # (K^3, 3)
    return translations


def sample_se3(N_R: int, N_t: int, t_amplitude: float, device: Device = 'cpu') -> Transform3d:
    R = super_fibonacci_spirals(N_R, device).contiguous()       # (N_R, 3, 3)
    t = sample_translations_grid(N_t, t_amplitude, device)      # (N_t^3, 3)
    t = t[t.norm(dim=1) <= 1].contiguous()                      # (N_t'^3 < N_t^3, 3)
    R_ = flatten(expand(R, len(t), dim=1))                      # (N_R * N_t'^3, 3, 3)
    t_ = flatten(expand(t, N_R, dim=0))                         # (N_R * N_t'^3, 3)
    se3_sampling = Transform3d(device=device).rotate(R_.mT).translate(t_)
    return se3_sampling


# +-------------------------------------------------------------------------------------------------------+ #
# |                                       SE(3) LOCAL MINIMA SEARCH                                       | #
# +-------------------------------------------------------------------------------------------------------+ #

def single_view_find_se3_local_minima(se3_knn_graph: SE3KnnGraph, values: Tensor) -> Tensor:
    neighbors = torch.stack([n['indices'] for n in se3_knn_graph.values()])  # type: ignore
    local_minima_indices = (values[:, None] <= values[neighbors]).all(dim=1).argwhere().squeeze(dim=1)
    return local_minima_indices[values[local_minima_indices].argsort()]


def parallel_find_se3_local_minima(se3_knn_graph: SE3KnnGraph, values: Tensor) -> list[Tensor]:
    """ All views in parallel: values is a tensor (num_views, se3_sampling_size). """
    neighbors = torch.stack([n['indices'] for n in se3_knn_graph.values()])  # type: ignore
    # boolean (N, L) =   (N, L, 1)     <=       (L, K)         (all)
    local_minima = (values[:, :, None] <= values[:, neighbors]).all(dim=2)
    local_minima_indices = [l.argwhere().squeeze(dim=1) for l in local_minima]
    local_minima_indices_sorted = [l[v[l].argsort()] for l, v in zip(local_minima_indices, values)]
    return local_minima_indices_sorted


def find_se3_local_minima_from_knn_graph(
    se3_knn_graph: SE3KnnGraph,
    values: Tensor,
    parallel: bool
) -> list[Tensor]:
    if parallel:
        return parallel_find_se3_local_minima(se3_knn_graph, values)
    return [single_view_find_se3_local_minima(se3_knn_graph, v) for v in values]


# +-------------------------------------------------------------------------------------------------------+ #
# |                                  SE(3) SAMPLING CONTAINER STRUCTURES                                  | #
# +-------------------------------------------------------------------------------------------------------+ #

class SE3Sampling:

    def __init__(self, N_R: int, N_t: int, t_amplitude: float, device: Optional[Device] = None) -> None:
        self.device = device if device is not None else default_device()
        self.N_R = int(N_R)
        self.N_t = int(N_t)
        self.t_amplitude = t_amplitude
        self.transforms = self.sample_se3()
        self.matrix = self.transforms.get_matrix()

    @property
    def desc(self) -> str:
        return f'N_R={self.N_R}_N_t={self.N_t}_t_amplitude={self.t_amplitude}'

    def __len__(self) -> int:
        return len(self.matrix)

    def sample_se3(self) -> Transform3d:
        raise NotImplementedError


class SE3RandomSampling(SE3Sampling):

    def generate_random_motions(self, n: int) -> Transform3d:
        R = random_rotations(n, device=self.device)
        t = 2 * self.t_amplitude * torch.rand(n, 3, device=self.device) - self.t_amplitude
        return Transform3d(device=self.device).rotate(R).translate(t)

    def sample_se3(self) -> Transform3d:
        return self.generate_random_motions(self.N_R)


class SE3UniformSampling(SE3Sampling):

    def sample_se3(self) -> Transform3d:
        return sample_se3(self.N_R, self.N_t, self.t_amplitude, self.device)


def make_se3_sampling(sampling: str, N_R: int, N_t: int, t_amplitude: float, device: Device) -> SE3Sampling:
    if sampling == 'random':
        return SE3RandomSampling(N_R, -1, t_amplitude, device)
    if sampling == 'uniform':
        if N_t < 0:
            alpha = torch.pi / (2 * t_amplitude)
            N_t = N_t_from_N_R(N_R, alpha, device)
        return SE3UniformSampling(N_R, N_t, t_amplitude, device)
    raise NotImplementedError


# +-------------------------------------------------------------------------------------------------------+ #
# |                                       SE(3) KNN GRAPH STRUCTURE                                       | #
# +-------------------------------------------------------------------------------------------------------+ #

class SE3SamplingKnnGraph:

    def __init__(
        self,
        se3: SE3Sampling,
        K: int,
        batch_size: int,
        cache_dir: Optional[str],
        verbose: bool,
        progress_bar: bool,
        monitor_vram: bool,
        gpu_index: int,
    ) -> None:
        self.se3 = se3
        self.K = K
        self.batch_size = batch_size
        self.verbose = verbose
        self.progress_bar = progress_bar
        self.monitor_vram = monitor_vram
        self.gpu_index = gpu_index
        self.cache_dir = cache_dir
        self.t_weight = (torch.pi / (2 * self.se3.t_amplitude)) ** 2
        self.get_knn_graph()
        self.local_minima_history: list[list[Tensor]] = []

    @property
    def nearest_neighbor_distances(self) -> Tensor:
        return torch.hstack([v['distances'][0] for v in self.knn_graph.values()])

    @property
    def farthest_neighbor_distances(self) -> Tensor:
        return torch.hstack([v['distances'][-1] for v in self.knn_graph.values()])

    def local_minima_search(
        self, values: Tensor, J: int | None, multiviews: bool, parallel: bool
    ) -> Tensor | list[Tensor]:
        if not multiviews:
            return single_view_find_se3_local_minima(self.knn_graph, values)[:J]
        local_minima = find_se3_local_minima_from_knn_graph(self.knn_graph, values, parallel)
        self.local_minima_history.append(local_minima)
        num_local_minima = [len(lm) for lm in local_minima]
        avg_num_local_minima = sum(num_local_minima) / len(num_local_minima)
        if J is not None and (avg_num_local_minima > 2 * J or avg_num_local_minima < J // 2) and self.verbose:
            print((f'WARNING: you requested the {J:,} best local minima, but {avg_num_local_minima:.2f} were '
                   'found on average.\nTry to adjust the number of requested minima '
                   'or the neighborhood size.'))
        return [lm[:J] for lm in local_minima]

    def make_knn_graph(self,) -> None:
        """ Note that each rotation is its own neighbor. """
        if self.batch_size < len(self.se3.matrix):
            print(':: Trying larger batch size for SE(3) pairwise geodesic distance computation.')
            batch_size = len(self.se3.matrix)
            try:
                k_min_distances, k_min_indices = batched_k_min_pairwise_se3_geodesic_distances(
                    self.se3.matrix, self.se3.matrix, self.t_weight, self.K,
                    batch_size, self.progress_bar, self.se3.device, self.monitor_vram, self.gpu_index
                )
            except RuntimeError:
                torch.cuda.empty_cache()
                torch.cuda.ipc_collect()
                k_min_distances, k_min_indices = batched_k_min_pairwise_se3_geodesic_distances(
                    self.se3.matrix, self.se3.matrix, self.t_weight, self.K,
                    self.batch_size, self.progress_bar, self.se3.device, self.monitor_vram, self.gpu_index
                )
        else:
            k_min_distances, k_min_indices = batched_k_min_pairwise_se3_geodesic_distances(
                self.se3.matrix, self.se3.matrix, self.t_weight, self.K,
                self.batch_size, self.progress_bar, self.se3.device, self.monitor_vram, self.gpu_index
            )
        k_min_indices = k_min_indices.long()
        # distances, indices = torch.stack(min_k_distances), torch.stack(min_k_indices)
        self.knn_graph: SE3KnnGraph = {i: {'indices': k_min_indices[i],
                                           'distances': k_min_distances[i]}  # type: ignore
                                       for i in range(len(k_min_indices))}

    def save_knn_graph(self) -> None:
        """ Store two tensors Indices and Distances such that:
            for all i in {1, ..., N_R * N_t^3}
            T[i]'s neighbors are T[Indices[i]], and geodesic distances between T[i] and T[Indices[i]] are
            Distances[i].
        """
        self.cache_dir = cast(str, self.cache_dir)
        here = Path(__file__).resolve().parent
        output_path = here / self.cache_dir
        output_path.mkdir(exist_ok=True)
        filename = f"se3_knn_lookup_table_indices_{self.se3.desc}_K={self.K}.pt"
        indices = torch.stack([self.knn_graph[i]['indices'] for i in range(len(self.se3))])
        torch.save(indices, output_path / filename)
        filename = f"se3_knn_lookup_table_distances_{self.se3.desc}_K={self.K}.pt"
        distances = torch.stack([self.knn_graph[i]['distances'] for i in range(len(self.se3))])
        torch.save(distances, output_path / filename)

    def make_and_save_knn_graph(self) -> None:
        self.make_knn_graph()
        self.save_knn_graph()

    def get_knn_graph(self) -> None:
        """ Search cached files on disk. If not found, create them. """
        if isinstance(self.se3, SE3RandomSampling):
            if self.verbose:
                print(':: Not loading / saving SE(3) k-nn graph since motions have been randomly sampled.')
            self.make_knn_graph()
            return
        if self.cache_dir is None:
            if self.verbose:
                print(':: Not loading / saving SE(3) k-nn graph since `cache_dir` is None.')
            self.make_knn_graph()
            return
        self.cache_dir = cast(str, self.cache_dir)
        here = Path(__file__).resolve().parent
        output_path = here / self.cache_dir
        pattern = f"se3_knn_lookup_table_indices_{self.se3.desc}_K=*.pt"
        for filename in output_path.glob(pattern):
            cached_K = int(filename.stem.split('=')[-1])
            if cached_K >= self.K:
                break
        else:
            if self.verbose:
                print((":: Cached SE(3) k-nn graph not found. It will be created on the fly and saved for "
                       "later use. This will occur extra runtime."))
            self.make_and_save_knn_graph()
            return
        if self.verbose:
            print(":: Using cached SE(3) knn-graph.")
        path = output_path / f"se3_knn_lookup_table_indices_{self.se3.desc}_K={cached_K}.pt"
        indices = torch.load(path, weights_only=True).long()
        path = output_path / f"se3_knn_lookup_table_distances_{self.se3.desc}_K={cached_K}.pt"
        angles = torch.load(path, weights_only=True)
        self.knn_graph: SE3KnnGraph = {i: {'indices': indices[i][:self.K], 'distances': angles[i][:self.K]}
                                       for i in range(len(indices))}
