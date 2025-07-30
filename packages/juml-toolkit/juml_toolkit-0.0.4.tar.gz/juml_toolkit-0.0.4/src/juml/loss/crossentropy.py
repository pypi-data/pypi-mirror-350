import torch
from juml.loss.base import Loss

class CrossEntropy(Loss):
    def forward(self, y, t):
        return torch.nn.functional.cross_entropy(y, t)

    def metric_batch(self, y, t):
        return torch.where(y.argmax(dim=-1) == t, 1, 0).sum().item()

    @classmethod
    def info(cls):
        return {"ylabel": "Loss"}

    @classmethod
    def metric_info(cls):
        return {"ylabel": "Accuracy", "ylim": [0, 1]}

    @classmethod
    def metric_higher_is_better(cls) -> bool:
        return True
