from __future__ import annotations
from typing import cast
import torch
from torch import Tensor
import pytorch3d
from packaging.version import Version
if Version(pytorch3d.__version__) < Version('0.7.8'):
    from .chamfer_newer_pytorch3d import chamfer_distance
else:
    from pytorch3d.loss import chamfer_distance
from .pcd import expand


def pointwise_single_directional_chamfer_distance(X: Tensor, Y: Tensor) -> Tensor:
    d, _ = chamfer_distance(X, Y, batch_reduction=None, point_reduction=None, single_directional=True)
    d = cast(Tensor, d)
    return d
    # nu = 2
    # welsch = 1 - (- 0.5 * (d / nu) ** 2).exp()
    # return welsch

# def pointwise_single_directional_chamfer_distance(X: Tensor, Y: Tensor) -> Tensor:
#     # d, _ = chamfer_distance(X, Y, batch_reduction=None, point_reduction=None, single_directional=True)
#     return torch.cdist(X, Y).min(dim=2).values


def chamfer_distances(X: Tensor, Y: Tensor, bidirectional: bool = False, trim_ratio: float = 0.) -> Tensor:
    d_x2y = pointwise_single_directional_chamfer_distance(X, Y)  # (B, N)
    if trim_ratio > 0:
        K = int((1 - trim_ratio) * X.shape[1])  # K = (1 - trim_ratio) * N_S
        # d_x2y = d_x2y.sort().values[:, :K]  # (B, K)
        d_x2y = d_x2y.topk(K, dim=1, largest=False).values  # (B, K)
    d_x2y = d_x2y.mean(dim=1)  # (B,)
    if not bidirectional:
        return d_x2y
    d_y2x = pointwise_single_directional_chamfer_distance(Y, X)
    if trim_ratio > 0:
        K = int((1 - trim_ratio) * Y.shape[1])  # K = (1 - trim_ratio) * N_M
        d_y2x = d_y2x.topk(K, dim=1, largest=False).values  # (B, K)
    d_y2x = d_y2x.mean(dim=1)  # (B,)
    return (d_x2y + d_y2x) / 2


def chamfer_distances_between_views_and_model(
    views: Tensor, model: Tensor, *, from_model: bool, bidirectional: bool, trim_ratio
) -> Tensor:
    # TODO: make compatible with class below
    model_expanded = expand(model, len(views), dim=0)
    # model_expanded = model.expand(len(views), -1, -1)
    inputs = (model_expanded, views) if from_model else (views, model_expanded)
    return chamfer_distances(*inputs, bidirectional, trim_ratio)


class ChamferDistance:

    def __init__(self, bidirectional: bool, trim_ratio: float | Tensor) -> None:
        self.bidirectional = bidirectional
        self.trim_ratio = trim_ratio.item() if isinstance(trim_ratio, Tensor) else trim_ratio

    def __call__(self, X: Tensor, Y: Tensor) -> Tensor:
        return chamfer_distances(X, Y, self.bidirectional, self.trim_ratio)


def compute_integral(
    sources: Tensor,
    models: Tensor,
    *, overlap_range: Tensor,
    bidirectional: bool
) -> Tensor:
    trim_ratios = 1 - overlap_range
    distances = torch.stack([chamfer_distances(sources, models,
                                               bidirectional=bidirectional, trim_ratio=t.item())
                             for t in trim_ratios]).T
    return torch.trapezoid(distances, x=overlap_range)
