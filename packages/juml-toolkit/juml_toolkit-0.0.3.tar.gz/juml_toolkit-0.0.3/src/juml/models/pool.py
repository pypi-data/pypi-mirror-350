import math
import torch
from jutility import cli
from juml.models.base import Model
from juml.models.linear import Linear

class Pooler(Model):
    def set_shapes(
        self,
        input_shape:  list[int],
        output_shape: list[int],
    ):
        raise NotImplementedError()

    def get_input_shape(self) -> list[int]:
        raise NotImplementedError()

    def get_input_dim(self, dim: int) -> int:
        input_shape = self.get_input_shape()
        return input_shape[dim]

    def unpool(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError()

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return []

class Identity(Pooler):
    def set_shapes(
        self,
        input_shape:  list[int],
        output_shape: list[int],
    ):
        self._output_shape = output_shape

    def get_input_shape(self) -> list[int]:
        return self._output_shape

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x

    def unpool(self, x: torch.Tensor) -> torch.Tensor:
        return x

class Unflatten(Pooler):
    def __init__(self, n: int):
        self._torch_module_init()
        self._n = n

    def set_shapes(
        self,
        input_shape:  list[int],
        output_shape: list[int],
    ):
        self._unflatten_shape = output_shape[-self._n:]
        self._input_shape = [
            *output_shape[:-self._n],
            math.prod(self._unflatten_shape),
        ]

    def get_input_shape(self) -> list[int]:
        return self._input_shape

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x.unflatten(-1, self._unflatten_shape)

    def unpool(self, x: torch.Tensor) -> torch.Tensor:
        return x.flatten(-self._n, -1)

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [cli.Arg("n", type=int, default=None)]

class Average2d(Pooler):
    def set_shapes(
        self,
        input_shape:  list[int],
        output_shape: list[int],
    ):
        self.linear = torch.nn.Linear(input_shape[-3], output_shape[-1])

    def forward(self, x_nchw: torch.Tensor) -> torch.Tensor:
        x_nci = x_nchw.flatten(-2, -1)
        x_nc  = x_nci.mean(dim=-1)
        x_no  = self.linear.forward(x_nc)
        return x_no

class Max2d(Pooler):
    def set_shapes(
        self,
        input_shape:  list[int],
        output_shape: list[int],
    ):
        self.linear = torch.nn.Linear(input_shape[-3], output_shape[-1])

    def forward(self, x_nchw: torch.Tensor) -> torch.Tensor:
        x_nci = x_nchw.flatten(-2, -1)
        x_nc  = x_nci.max(dim=-1).values
        x_no  = self.linear.forward(x_nc)
        return x_no

class SoftmaxAverage2d(Pooler):
    def set_shapes(
        self,
        input_shape:  list[int],
        output_shape: list[int],
    ):
        self.f_p = Linear(input_shape[-3], 1)
        self.f_x = Linear(input_shape[-3], output_shape[-1])

    def forward(self, x_nchw: torch.Tensor) -> torch.Tensor:
        x_nic   = x_nchw.flatten(-2, -1).transpose(-1, -2)
        p_ni1   = self.f_p.forward(x_nic)
        p_n1i   = p_ni1.squeeze(-1).unsqueeze(-2)
        x_n1c   = torch.softmax(p_n1i, dim=-1) @ x_nic
        x_nc    = x_n1c.squeeze(-2)
        x_no    = self.f_x.forward(x_nc)
        return x_no

class LinearSet2d(Pooler):
    def set_shapes(
        self,
        input_shape:  list[int],
        output_shape: list[int],
    ):
        self.linear = Linear(input_shape[-3], output_shape[-1])

    def forward(self, x_nchw: torch.Tensor) -> torch.Tensor:
        x_npc = x_nchw.flatten(-2, -1).transpose(-1, -2)
        x_npo = self.linear.forward(x_npc)
        return x_npo

class GatedLinearSet2d(Pooler):
    def set_shapes(
        self,
        input_shape:  list[int],
        output_shape: list[int],
    ):
        self.f_p = Linear(input_shape[-3], 1)
        self.f_x = Linear(input_shape[-3], output_shape[-1])

    def forward(self, x_nchw: torch.Tensor) -> torch.Tensor:
        x_npc = x_nchw.flatten(-2, -1).transpose(-1, -2)
        p_np1 = self.f_p.forward(x_npc)
        x_npo = self.f_x.forward(x_npc)
        x_npo = torch.sigmoid(p_np1) * x_npo
        return x_npo

class SetAverage(Pooler):
    def set_shapes(
        self,
        input_shape:  list[int],
        output_shape: list[int],
    ):
        self.input_shape = input_shape
        self.linear = torch.nn.Linear(input_shape[-1], output_shape[-1])

    def get_input_shape(self) -> list[int]:
        return self.input_shape

    def forward(self, x_npd: torch.Tensor) -> torch.Tensor:
        x_nd = x_npd.mean(dim=-2)
        x_no = self.linear.forward(x_nd)
        return x_no

def get_types() -> list[type[Pooler]]:
    return [
        Identity,
        Unflatten,
        Average2d,
        Max2d,
        SoftmaxAverage2d,
        LinearSet2d,
        GatedLinearSet2d,
        SetAverage,
    ]

def get_cli_choice() -> cli.ObjectChoice:
    return cli.ObjectChoice(
        "pooler",
        *[pool_type.get_cli_arg() for pool_type in get_types()],
        default="Identity",
    )
