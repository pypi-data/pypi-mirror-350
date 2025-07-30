import torch
import torch.utils.data
from jutility import util

class DataSplit(torch.utils.data.Dataset):
    def __init__(self, x: torch.Tensor, t: torch.Tensor, n: int):
        self.x = x
        self.t = t
        self.n = n

    def __getitem__(self, index):
        return self.x[index], self.t[index]

    def __len__(self):
        return self.n

    def __repr__(self):
        return util.format_type(
            type(self),
            x_shape=list(self.x.shape),
            t_shape=list(self.t.shape),
            n=self.n,
        )
