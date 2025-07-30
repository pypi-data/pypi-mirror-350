import torch
from juml.loss.mse import Mse

class AlignedSetMse(Mse):
    def forward(self, y_npo: torch.Tensor, t_npo: torch.Tensor):
        e_npo = self.weights * (y_npo - t_npo)
        return e_npo.square().sum(dim=-1).mean()

    def metric_batch(self, y_npo: torch.Tensor, t_npo: torch.Tensor):
        e_npo = self.weights * (y_npo - t_npo)
        return e_npo.square().mean(dim=-2).sum().item()

    @classmethod
    def needs_weights(cls) -> bool:
        return True
