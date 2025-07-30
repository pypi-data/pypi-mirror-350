import math
import torch
from juml.models.base import Model

class Linear(Model):
    def __init__(
        self,
        input_dim:  int,
        output_dim: int,
        w_scale:    (float | None)=None,
    ):
        if w_scale is None:
            w_scale = 1 / math.sqrt(input_dim)

        w_shape = [input_dim, output_dim]
        self._torch_module_init()
        self.w_io = torch.nn.Parameter(torch.normal(0, w_scale, w_shape))
        self.b_o  = torch.nn.Parameter(torch.zeros(output_dim))

    def forward(self, x_ni: torch.Tensor) -> torch.Tensor:
        x_no = x_ni @ self.w_io + self.b_o
        return x_no

    def init_batch(
        self,
        x:      torch.Tensor,
        t:      (torch.Tensor | None),
        eps:    float=1e-5,
    ):
        with torch.no_grad():
            self.b_o.zero_()
            if t is None:
                x = x.flatten(0, -2)
                self.w_io *= 1 / (eps + x.std(-2).unsqueeze(-1))
                y = self.forward(x)
                self.w_io *= 1 / (eps + y.std(-2).unsqueeze(-2))
                y = self.forward(x)
                y_lo = y.quantile(0.01, dim=-2)
                y_hi = y.quantile(0.99, dim=-2)
                r = torch.rand(self.b_o.shape)
                t = y_lo + r * (y_hi - y_lo)
                self.b_o.copy_(-t)
            else:
                x = x.flatten(0, -2)
                t = t.flatten(0, -2)
                xm = x.mean(-2)
                tm = t.mean(-2)
                w, _, _, _ = torch.linalg.lstsq(x - xm, t - tm)
                self.w_io.copy_(w)
                self.b_o.copy_(tm - self.forward(xm))
