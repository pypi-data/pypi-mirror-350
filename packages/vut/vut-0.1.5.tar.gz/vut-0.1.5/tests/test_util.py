import numpy as np
import pytest
import torch

from vut.util import init_seed, to_list, to_np, to_tensor, unique


def test_init_seed__same_values():
    init_seed(42)
    data = np.random.rand(1000)
    init_seed(42)
    expected = np.random.rand(1000)
    assert np.array_equal(data, expected), (
        "Random data should be the same after re-initializing the seed"
    )


def test_init_seed__different_values():
    init_seed(42)
    data1 = np.random.rand(1000)
    init_seed(43)
    data2 = np.random.rand(1000)
    assert not np.array_equal(data1, data2), (
        "Random data should be different after changing the seed"
    )


test_case_unique = [
    # empty
    ([], []),
    # single element
    ([1], [1]),
    # multiple elements
    ([1, 2, 3], [1, 2, 3]),
    # duplicates
    ([1, 2, 2, 3], [1, 2, 3]),
    ([1, 1, 1], [1]),
    # mixed types
    ([1, 2.0, 3], [1, 2.0, 3]),
    # order preservation
    ([3, 1, 2, 1], [3, 1, 2]),
    ([1, 3, 1, 2, 4, 3, 2], [1, 3, 2, 4]),
]


@pytest.mark.parametrize(
    "data, expected",
    test_case_unique,
)
def test_unique__list(data, expected):
    assert unique(data) == expected


@pytest.mark.parametrize(
    "data, expected",
    test_case_unique,
)
def test_unique__ndarray(data, expected):
    data = np.array(data)
    expected = np.array(expected)
    assert np.array_equal(unique(data), expected)


@pytest.mark.parametrize(
    "data, expected",
    test_case_unique,
)
def test_unique__tensor(data, expected):
    data = torch.tensor(data)
    expected = torch.tensor(expected)
    assert torch.equal(unique(data), expected)


def test_unique__unsupported_type():
    with pytest.raises(TypeError):
        unique("unsupported type")


def test_to_list__list():
    data = [1, 2, 3]
    result = to_list(data)
    assert result == data, "Should return the same list"


def test_to_list__ndarray():
    data = np.array([1, 2, 3])
    result = to_list(data)
    assert result == data.tolist(), "Should return the same list"


def test_to_list__tensor():
    data = torch.tensor([1, 2, 3])
    result = to_list(data)
    assert result == data.tolist(), "Should return the same list"


def test_to_list__unsupported_type():
    with pytest.raises(TypeError):
        to_list("unsupported type")


def test_to_np__list():
    data = [1, 2, 3]
    result = to_np(data)
    assert np.array_equal(result, np.array(data)), "Should return the same numpy array"


def test_to_np__ndarray():
    data = np.array([1, 2, 3])
    result = to_np(data)
    assert np.array_equal(result, data), "Should return the same numpy array"


def test_to_np__tensor():
    data = torch.tensor([1, 2, 3])
    result = to_np(data)
    assert np.array_equal(result, data.numpy()), "Should return the same numpy array"


def test_to_np__unsupported_type():
    with pytest.raises(TypeError):
        to_np("unsupported type")


def test_to_tensor__list():
    data = [1, 2, 3]
    result = to_tensor(data)
    assert torch.equal(result, torch.tensor(data)), "Should return the same tensor"


def test_to_tensor__ndarray():
    data = np.array([1, 2, 3])
    result = to_tensor(data)
    assert torch.equal(result, torch.tensor(data)), "Should return the same tensor"


def test_to_tensor__tensor():
    data = torch.tensor([1, 2, 3])
    result = to_tensor(data)
    assert torch.equal(result, data), "Should return the same tensor"


def test_to_tensor__unsupported_type():
    with pytest.raises(TypeError):
        to_tensor("unsupported type")
