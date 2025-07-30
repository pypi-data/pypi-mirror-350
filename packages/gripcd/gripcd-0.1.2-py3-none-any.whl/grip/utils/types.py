from __future__ import annotations
from typing import Callable
from typing_extensions import TypeAlias

import torch
from torch import Tensor


# _________________________________________________________________________________________________________ #

SE3KnnGraph: TypeAlias = "dict[int, dict[str, Tensor]]"
Device: TypeAlias = "str | torch.device"

# _________________________________________________________________________________________________________ #

Losses: TypeAlias = Tensor
RigidMotion: TypeAlias = Tensor
PointClouds: TypeAlias = Tensor

RegistrationFn: TypeAlias = Callable[[PointClouds, PointClouds], RigidMotion]
Criterion: TypeAlias = Callable[[PointClouds, PointClouds], Losses]
