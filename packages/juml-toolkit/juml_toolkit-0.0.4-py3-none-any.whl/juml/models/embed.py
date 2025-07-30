import math
import torch
from jutility import cli
from juml.models.base import Model

class Embedder(Model):
    def set_input_shape(self, input_shape: list[int]):
        raise NotImplementedError()

    def get_output_shape(self) -> list[int]:
        raise NotImplementedError()

    def get_output_dim(self, dim: int) -> int:
        output_shape = self.get_output_shape()
        return output_shape[dim]

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return []

class Identity(Embedder):
    def set_input_shape(self, input_shape: list[int]):
        self._input_shape = input_shape

    def get_output_shape(self) -> list[int]:
        return self._input_shape

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x

class Flatten(Embedder):
    def __init__(self, n: int):
        self._torch_module_init()
        self._n = n

    def set_input_shape(self, input_shape: list[int]):
        self._input_shape = input_shape

    def get_output_shape(self) -> list[int]:
        return [
            *self._input_shape[:-self._n],
            math.prod(self._input_shape[-self._n:]),
        ]

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return x.flatten(-self._n, -1)

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [cli.Arg("n", type=int, default=None)]

class CoordConv(Embedder):
    def set_input_shape(self, input_shape: list[int]):
        self._torch_module_init()
        c, h, w = input_shape[-3:]
        x_1w    = torch.linspace(-1, 1, w).unsqueeze(-2)
        y_h1    = torch.linspace(-1, 1, h).unsqueeze(-1)
        x_hw    = torch.tile(x_1w, [h, 1])
        y_hw    = torch.tile(y_h1, [1, w])
        xy_2hw  = torch.stack([x_hw, y_hw], dim=-3)
        self._coord_tensor = torch.nn.Parameter(xy_2hw, requires_grad=False)
        self._coord_shape  = list(self._coord_tensor.shape)
        self._output_shape = input_shape[:-3] + [c + 2, h, w]

    def get_output_shape(self) -> list[int]:
        return self._output_shape

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batched_shape = list(x.shape[:-3]) + self._coord_shape
        batched_coord_tensor = self._coord_tensor.expand(batched_shape)
        return torch.concat([x, batched_coord_tensor], dim=-3)

def get_types() -> list[type[Embedder]]:
    return [
        Identity,
        Flatten,
        CoordConv,
    ]

def get_cli_choice() -> cli.ObjectChoice:
    return cli.ObjectChoice(
        "embedder",
        *[embed_type.get_cli_arg() for embed_type in get_types()],
        default="Identity",
    )
