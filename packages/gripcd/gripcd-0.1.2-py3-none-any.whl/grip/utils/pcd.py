from __future__ import annotations
import torch
from torch import Tensor


# _________________________________________________ Center ________________________________________________ #

def center(pointclouds: Tensor) -> tuple[Tensor, Tensor]:
    """ Center each element in a batch of point clouds (substract the mean over the second dim).

    Args:
        pointclouds (Tensor): Batch of point clouds. Batch `(B, N, *)`.

    Returns:
        Batch of centered point clouds, and batch of computed means (with dim kept) `(B, 1, *)`.
    """
    means = pointclouds.mean(dim=1, keepdim=True)
    centered_pointclouds = pointclouds - means
    return centered_pointclouds, means


# _________________________________________________ Scale _________________________________________________ #

def scale(pointclouds: Tensor, values: Tensor) -> Tensor:
    """ Apply a unique scaling factor to each point cloud in the provided batch.

    Args:
        pointclouds (Tensor): Batch of point clouds `(B, N, *)`.
        values (Tensor): Batch of scalar scaling values `(B,)`.

    Returns:
        Batch of scaled point clouds `(B, N, *)`.
    """
    return pointclouds * values[:, None, None].to(pointclouds.device)


# ___________________________________________ Pairwise Max Norm ___________________________________________ #

def pairwise_max_norm(pointclouds1: Tensor, pointclouds2: Tensor) -> tuple[Tensor, Tensor, Tensor]:
    """ Scale each pair of elements of the two batches by their maximal norm.

    !!! Warning
        `pointclouds1` and `pointclouds2` MUST have the same length.

    Args:
        pointclouds1 (Tensor): Batch of point clouds `(B, N, *)`.
        pointclouds2 (Tensor): Batch of point clouds `(B, M, *)`.

    Returns:
        The two batches of normalized point clouds.
    """
    assert len(pointclouds1) == len(pointclouds2), 'Inputs must be of same length.'
    pointclouds1_c, _ = center(pointclouds1)
    pointclouds2_c, _ = center(pointclouds2)
    norms1 = pointclouds1_c.norm(dim=2).amax(dim=1)  # B
    norms2 = pointclouds2_c.norm(dim=2).amax(dim=1)  # B
    max_norms = torch.stack((norms1, norms2)).amax(dim=0)  # (2, B) -> B
    scales = 1 / max_norms
    pointclouds1_n = scale(pointclouds1, scales)
    pointclouds2_n = scale(pointclouds2, scales)
    return pointclouds1_n, pointclouds2_n, scales


# _______________________________________________ Max Norm ________________________________________________ #


def max_norm(pointclouds: Tensor) -> tuple[Tensor, Tensor]:
    """ Apply the same scaling factor to all the point clouds in the batch, so that the biggest has a norm
        of 1.

    Args:
        pointclouds (Tensor): Batch of point clouds `(B, N, *)`.

    Returns:
        Batch of normalized point clouds.
    """
    pointclouds_c, _ = center(pointclouds)
    max_norm = pointclouds_c.norm(dim=2).amax(dim=1).max()
    scales = 1 / max_norm.repeat(len(pointclouds))
    pointclouds_n = scale(pointclouds, scales)
    return pointclouds_n, scales


def rescale_scene(
    sources: Tensor, models: Tensor, target_scale: float | Tensor
) -> tuple[Tensor, Tensor, Tensor]:
    """ TODO: docstring """
    assert len(sources) == len(models), 'Sources & Models must be of same length.'
    fused = torch.hstack((sources, models))
    max_norms = fused.norm(dim=2).amax(dim=1)
    scales = target_scale / max_norms
    return scale(sources, scales), scale(models, scales), scales


# ___________________________________ Flatten, Unflatten, Stack, Expand ___________________________________ #

def flatten(x: Tensor) -> Tensor:
    return x.flatten(start_dim=0, end_dim=1)


def unflatten(x: Tensor, sizes: tuple[int, int]) -> Tensor:
    return x.unflatten(0, sizes)


def expand(x: Tensor, k: int, dim: int) -> Tensor:
    """ Expand the n-th dim k times. Juste a utility to guess expanded size.

    Args:
        x (Tensor): Data to expand.
        k (int): Number of repetitions.

    Returns:
        Expanded data. One dimension more than input, at index = dim.
        e.g.: if X is (N, M, P), expand(X, K, 1) is (N, K, M, P).
    """
    n = x.ndim
    return x.unsqueeze(dim).expand(*(dim * (-1,)), k, *((n - dim) * (-1,)))
