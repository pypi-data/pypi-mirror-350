import torch
from jutility import cli
from juml.loss.base import Loss

class ChamferMse(Loss):
    def chamfer_components(self, y_nqc: torch.Tensor, t_npc: torch.Tensor):
        t_np1c  = t_npc.unsqueeze(-2)
        y_n1qc  = y_nqc.unsqueeze(-3)
        e_npqc  = self.weights * (t_np1c - y_n1qc)
        mse_npq = e_npqc.square().sum(dim=-1)
        mse_np  = mse_npq.min(dim=-1).values
        mse_nq  = mse_npq.min(dim=-2).values
        return mse_np, mse_nq

    def forward(self, y, t):
        mse_np, mse_nq = self.chamfer_components(y, t)
        return mse_np.mean() + mse_nq.mean()

    def metric_batch(self, y, t):
        mse_np, mse_nq = self.chamfer_components(y, t)
        return (
            mse_np.mean(dim=-1).sum().item() +
            mse_nq.mean(dim=-1).sum().item()
        )

    @classmethod
    def info(cls):
        return {"ylabel": "Chamfer MSE", "log_y": True}

    @classmethod
    def needs_weights(cls) -> bool:
        return True

    @classmethod
    def get_cli_arg(cls):
        return cli.ObjectArg(cls, tag="CH")
