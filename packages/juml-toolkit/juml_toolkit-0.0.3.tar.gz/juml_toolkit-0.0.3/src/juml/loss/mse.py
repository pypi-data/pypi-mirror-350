import torch
from juml.loss.base import Loss

class Mse(Loss):
    def forward(self, y, t):
        return (y - t).square().sum(dim=-1).mean()

    def metric_batch(self, y, t):
        return (y - t).square().sum().item()

    @classmethod
    def info(cls):
        return {"ylabel": "MSE", "log_y": True}
