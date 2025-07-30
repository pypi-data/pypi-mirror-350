import torch
from torch.utils.data import Dataset


class NoopDataset(Dataset):
    def __init__(self, *args, **kwargs):
        pass

    def __len__(self):
        return 0

    def __getitem__(self, index):
        return torch.tensor(0)
