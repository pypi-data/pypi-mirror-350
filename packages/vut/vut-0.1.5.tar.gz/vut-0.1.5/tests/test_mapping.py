import numpy as np
import pytest
import torch

from vut.mapping import to_class_index, to_class_name


def test_to_class_name():
    mapping = {
        0: "cat",
        1: "dog",
        2: "bird",
    }
    indices = [0, 1, 2]
    expected = ["cat", "dog", "bird"]
    result = to_class_name(indices, mapping)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_to_class_name__empty():
    mapping = {
        0: "cat",
        1: "dog",
        2: "bird",
    }
    indices = []
    expected = []
    result = to_class_name(indices, mapping)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_to_class_name__unknown_index():
    mapping = {
        0: "cat",
        1: "dog",
        2: "bird",
    }
    indices = [0, 1, 3]
    expected = ["cat", "dog", ""]
    result = to_class_name(indices, mapping)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_to_class_name__invalid_shape():
    mapping = {
        0: "cat",
        1: "dog",
        2: "bird",
    }
    indices = [[0, 1], [2]]
    with pytest.raises(AssertionError):
        to_class_name(indices, mapping)


def test_to_class_name__ndarray():
    mapping = {
        0: "cat",
        1: "dog",
        2: "bird",
    }
    indices = np.array([0, 1, 2])
    expected = ["cat", "dog", "bird"]
    result = to_class_name(indices, mapping)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_to_class_name__invalid_ndarray():
    mapping = {
        0: "cat",
        1: "dog",
        2: "bird",
    }
    indices = np.array([[0, 1], [2, 3]])
    with pytest.raises(AssertionError):
        to_class_name(indices, mapping)


def test_to_class_name__tensor():
    mapping = {
        0: "cat",
        1: "dog",
        2: "bird",
    }
    indices = torch.tensor([0, 1, 2])
    expected = ["cat", "dog", "bird"]
    result = to_class_name(indices, mapping)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_to_class_name__invalid_tensor():
    mapping = {
        0: "cat",
        1: "dog",
        2: "bird",
    }
    indices = torch.tensor([[0, 1], [2, 3]])
    with pytest.raises(AssertionError):
        to_class_name(indices, mapping)


def test_to_class_index():
    mapping = {
        "cat": 0,
        "dog": 1,
        "bird": 2,
    }
    names = ["cat", "dog", "bird"]
    expected = [0, 1, 2]
    result = to_class_index(names, mapping)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_to_class_index__empty():
    mapping = {
        "cat": 0,
        "dog": 1,
        "bird": 2,
    }
    names = []
    expected = []
    result = to_class_index(names, mapping)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_to_class_index__unknown_name():
    mapping = {
        "cat": 0,
        "dog": 1,
        "bird": 2,
    }
    names = ["cat", "dog", "fish"]
    expected = [0, 1, -1]
    result = to_class_index(names, mapping)
    assert result == expected, f"Expected {expected}, but got {result}"


def test_to_class_index__invalid_shape():
    mapping = {
        "cat": 0,
        "dog": 1,
        "bird": 2,
    }
    names = [["cat", "dog"], ["bird"]]
    with pytest.raises(AssertionError):
        to_class_index(names, mapping)
