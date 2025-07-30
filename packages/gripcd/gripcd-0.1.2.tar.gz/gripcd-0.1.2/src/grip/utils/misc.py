from typing import Optional
from tqdm.auto import tqdm
import torch
from torch import Tensor
from pytorch3d.transforms import Transform3d
import nvidia_smi  # nvidia-ml-py3


# _________________________________________________________________________________________________________ #

def default_device() -> torch.device:
    return torch.device('cuda' if torch.cuda.is_available() else 'cpu')


# _________________________________________________________________________________________________________ #

def bytes2human(number: int, decimal_unit: bool = True) -> str:
    """ Convert number of bytes in a human readable string.
    >>> bytes2human(10000, True)
    '10.00 KB'
    >>> bytes2human(10000, False)
    '9.77 KiB'
    Args:
        number (int): Number of bytes
        decimal_unit (bool): If specified, use 1 kB (kilobyte)=10^3 bytes.
            Otherwise, use 1 KiB (kibibyte)=1024 bytes
    Returns:
        str: Bytes converted in readable string
    """
    symbols = ['K', 'M', 'G', 'T', 'P', 'E', 'Z', 'Y']
    symbol_values = [(symbol, 1000 ** (i + 1) if decimal_unit else (1 << (i + 1) * 10))
                     for i, symbol in enumerate(symbols)]
    for symbol, value in reversed(symbol_values):
        if number >= value:
            suffix = "B" if decimal_unit else "iB"
            return f"{float(number)/value:.2f}{symbol}{suffix}"
    return f"{number} B"


# _________________________________________________________________________________________________________ #

def batch(
    function,
    *,
    args,
    out,
    batch_size,
    progress_bar: bool = False,
    desc: Optional[str] = None,
    monitor_vram: bool = False,
    gpu_index: int = 0,
) -> None:
    """ All args must have same lengths. Fill `out` tensor inplace.
        e.g: batch(sum, args=(X, Y), out=torch.empty(1000), batch_size=16).
    """
    # return merge([function(*batched_args)
    #               for batched_args in zip(*[arg.split(batch_size) for arg in args])])
    n = len(args[0])
    num_batches = (n + batch_size - 1) // batch_size
    iterations = tqdm(range(num_batches), desc=desc) if progress_bar else range(num_batches)
    if monitor_vram and progress_bar:
        nvidia_smi.nvmlInit()
        handle = nvidia_smi.nvmlDeviceGetHandleByIndex(gpu_index)
    for batch_idx in iterations:
        start_idx = batch_idx * batch_size
        end_idx = min(start_idx + batch_size, n)
        idx = slice(start_idx, end_idx)
        out[idx] = function(*[arg[idx] for arg in args])
        if progress_bar and monitor_vram:
            gpu_info = nvidia_smi.nvmlDeviceGetMemoryInfo(handle)  # type: ignore
            iterations.set_postfix_str(f'VRAM: {bytes2human(gpu_info.used)}')  # type: ignore


# _________________________________________________________________________________________________________ #

def apply_transform(M: Tensor, X: Tensor) -> Tensor:
    """ M is a batch (B,4,4) of homogeneous rigid motion matrices, X is a batch of pointclouds (B, N, 3)
        or a single one (N, 3).
    """
    return Transform3d(matrix=M).transform_points(X)
    # print(X.shape, M.shape)
    # return X.bmm(M[:, :3, :3]) + M[:, 3, :3]
