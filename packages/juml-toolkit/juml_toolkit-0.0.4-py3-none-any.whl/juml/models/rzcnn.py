import torch
from jutility import cli
from juml.models.base import Model
from juml.models.sequential import Sequential
from juml.models.embed import Embedder
from juml.models.pool import Pooler

class RzCnn(Sequential):
    def __init__(
        self,
        input_shape:        list[int],
        output_shape:       list[int],
        kernel_size:        int,
        model_dim:          int,
        expand_ratio:       float,
        num_stages:         int,
        blocks_per_stage:   int,
        stride:             int,
        embedder:           Embedder,
        pooler:             Pooler,
    ):
        self._init_sequential(embedder, pooler)
        self.embed.set_input_shape(input_shape)
        self.pool.set_shapes([model_dim, None, None], output_shape)

        layer = torch.nn.Conv2d(
            in_channels=self.embed.get_output_dim(-3),
            out_channels=model_dim,
            kernel_size=kernel_size,
            stride=stride,
            padding=0,
        )
        self.layers.append(layer)

        for _ in range(num_stages - 1):
            for _ in range(blocks_per_stage - 1):
                layer = ReZeroCnnLayer(model_dim, expand_ratio, kernel_size)
                self.layers.append(layer)

            layer = torch.nn.Conv2d(
                in_channels=model_dim,
                out_channels=model_dim,
                kernel_size=kernel_size,
                stride=stride,
                padding=0,
            )
            self.layers.append(layer)

        for _ in range(blocks_per_stage):
            layer = ReZeroCnnLayer(model_dim, expand_ratio, kernel_size)
            self.layers.append(layer)

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [
            cli.Arg("kernel_size",      type=int,   default=5),
            cli.Arg("model_dim",        type=int,   default=64),
            cli.Arg("expand_ratio",     type=float, default=2.0, tag="x"),
            cli.Arg("num_stages",       type=int,   default=3),
            cli.Arg("blocks_per_stage", type=int,   default=2),
            cli.Arg("stride",           type=int,   default=2),
        ]

class ReZeroCnnLayer(Model):
    def __init__(
        self,
        model_dim:      int,
        expand_ratio:   float,
        kernel_size:    int,
    ):
        self._torch_module_init()
        expand_dim = int(model_dim * expand_ratio)
        padding = kernel_size // 2

        self.conv_1 = torch.nn.Conv2d(
            in_channels=model_dim,
            out_channels=model_dim,
            kernel_size=kernel_size,
            stride=1,
            padding=padding,
            groups=model_dim,
        )
        self.conv_2 = torch.nn.Conv2d(
            in_channels=model_dim,
            out_channels=expand_dim,
            kernel_size=1,
            stride=1,
            padding=0,
            groups=1,
        )
        self.conv_3 = torch.nn.Conv2d(
            in_channels=expand_dim,
            out_channels=model_dim,
            kernel_size=1,
            stride=1,
            padding=0,
            groups=1,
        )
        self.scale = torch.nn.Parameter(torch.tensor(0.0))

    def forward(self, x_nmhw: torch.Tensor) -> torch.Tensor:
        res_nmhw = self.conv_1.forward(x_nmhw)
        res_nehw = self.conv_2.forward(res_nmhw)
        res_nehw = torch.relu(res_nehw)
        res_nmhw = self.conv_3.forward(res_nehw)
        x_nmhw = x_nmhw + (self.scale * res_nmhw)
        return x_nmhw
