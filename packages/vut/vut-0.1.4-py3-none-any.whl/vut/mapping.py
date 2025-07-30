import numpy as np
import torch
from numpy.typing import NDArray
from torch import Tensor


def to_class_name(
    x: list | NDArray | Tensor, index_to_text: dict[int, str]
) -> list[str]:
    """Convert class indices to class names.

    Args:
        x (list | NDArray | Tensor): The input data containing class indices.
        index_to_text (dict[int, str]): A mapping from class indices to class names.

    Raises:
        TypeError: If the input type is unsupported.

    Returns:
        list[str]: A list of class names corresponding to the input indices.
    """
    if len(x) == 0:
        return []
    if isinstance(x, list):
        assert not isinstance(x[0], list), "List must be 1D"
        return [index_to_text.get(i, "") for i in x]
    if isinstance(x, np.ndarray):
        assert x.ndim == 1, "Array must be 1D"
        x = x.tolist()
        return [index_to_text.get(i, "") for i in x]
    if isinstance(x, torch.Tensor):
        assert x.ndim == 1, "Tensor must be 1D"
        x = x.detach().cpu().tolist()
        return [index_to_text.get(i, "") for i in x]


def to_class_index(x: list[str], text_to_index: dict[str, int]) -> list[int]:
    """Convert class names to class indices.

    Args:
        x (list[str]): The input data containing class names.
        text_to_index (dict[str, int]): A mapping from class names to class indices.

    Raises:
        TypeError: If the input type is unsupported.

    Returns:
        list[int]: A list of class indices corresponding to the input class names.
    """
    if len(x) == 0:
        return []
    assert not isinstance(x[0], list), "List must be 1D"
    return [text_to_index.get(i, -1) for i in x]
