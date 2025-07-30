import random

import numpy as np
import torch
from numpy.typing import NDArray
from torch import Tensor


def init_seed(seed: int = 42) -> None:
    """Initialize the random seed for reproducibility.

    Args:
        seed (int, optional): Seed value for random number generation. Defaults to 42.
    """
    torch.backends.cudnn.enabled = True
    torch.backends.cudnn.benchmark = False
    torch.backends.cudnn.deterministic = True
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
        torch.cuda.manual_seed(seed)


def unique(lst: list | NDArray | Tensor) -> list | NDArray | Tensor:
    """Return unique elements from the input list, NDArray, or Tensor while preserving order.

    Args:
        lst (list | NDArray | Tensor): Input list, NDArray, or Tensor to find unique elements from. Dimension size must be 1.

    Returns:
        list | NDArray | Tensor: Unique elements.
    """
    if isinstance(lst, list):
        return list(dict.fromkeys(lst))

    if isinstance(lst, np.ndarray):
        assert lst.ndim == 1, "Only 1D arrays are supported"
        _, indices = np.unique(lst, return_index=True)
        return lst[np.sort(indices)]

    if isinstance(lst, torch.Tensor):
        assert lst.ndim == 1, "Only 1D tensors are supported"
        # TODO: implement a more efficient way to get unique elements using torch
        return torch.tensor(
            list(dict.fromkeys(lst.cpu().tolist())),
            dtype=lst.dtype,
            device=lst.device,
        )

    raise TypeError(
        f"Unsupported type: {type(lst)}. Supported types are list, NDArray, and Tensor."
    )


def to_list(x: list | NDArray | Tensor) -> list:
    """Convert input to list.

    Args:
        x (list | NDArray | Tensor): Input to convert.

    Returns:
        list: Converted list.
    """
    if isinstance(x, list):
        return x

    if isinstance(x, np.ndarray):
        return x.tolist()

    if isinstance(x, torch.Tensor):
        return x.cpu().tolist()

    raise TypeError(
        f"Unsupported type: {type(x)}. Supported types are list, NDArray, and Tensor."
    )


def to_np(x: list | NDArray | Tensor) -> NDArray:
    """Convert input to numpy array.

    Args:
        x (list | NDArray | Tensor): Input to convert.

    Returns:
        NDArray: Converted numpy array.
    """
    if isinstance(x, list):
        return np.array(x)

    if isinstance(x, np.ndarray):
        return x

    if isinstance(x, torch.Tensor):
        return x.detach().cpu().numpy()

    raise TypeError(
        f"Unsupported type: {type(x)}. Supported types are list, NDArray, and Tensor."
    )


def to_tensor(x: list | NDArray | Tensor) -> Tensor:
    """Convert input to PyTorch tensor.

    Args:
        x (list | NDArray | Tensor): Input to convert.

    Returns:
        Tensor: Converted PyTorch tensor.
    """
    if isinstance(x, list):
        return torch.tensor(x)

    if isinstance(x, np.ndarray):
        return torch.from_numpy(x)

    if isinstance(x, torch.Tensor):
        return x

    raise TypeError(
        f"Unsupported type: {type(x)}. Supported types are list, NDArray, and Tensor."
    )
