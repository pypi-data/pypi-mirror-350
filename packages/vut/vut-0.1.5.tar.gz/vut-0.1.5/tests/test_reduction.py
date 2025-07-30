import numpy as np

from vut.reduction import compute_tsne


def test_compute_tsne():
    data = np.random.rand(10, 100)
    result = compute_tsne(data)
    assert result.shape == (10, 2)


def test_compute_tsne__small_dataset():
    data = np.random.rand(5, 10)
    result = compute_tsne(data)
    assert result.shape == (5, 2)
