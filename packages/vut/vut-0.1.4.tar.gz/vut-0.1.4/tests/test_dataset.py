import torch

from vut.dataset import NoopDataset


def test_noop_dataset():
    dataset = NoopDataset()
    assert len(dataset) == 0
    assert dataset[0] == torch.tensor(0)
