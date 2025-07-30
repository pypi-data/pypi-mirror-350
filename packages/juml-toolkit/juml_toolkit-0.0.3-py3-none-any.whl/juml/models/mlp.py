import torch
from jutility import cli
from juml.models.base import Model
from juml.models.sequential import Sequential
from juml.models.embed import Embedder
from juml.models.pool import Pooler
from juml.models.linear import Linear

class Mlp(Sequential):
    def __init__(
        self,
        input_shape:    list[int],
        output_shape:   list[int],
        hidden_dim:     int,
        depth:          int,
        embedder:       Embedder,
        pooler:         Pooler,
    ):
        self._init_sequential(embedder, pooler)
        self.embed.set_input_shape(input_shape)
        self.pool.set_shapes([], output_shape)

        layer_input_dim = self.embed.get_output_dim(-1)
        for _ in range(depth):
            layer = ReluMlpLayer(layer_input_dim, hidden_dim)
            self.layers.append(layer)
            layer_input_dim = hidden_dim

        layer_output_dim = self.pool.get_input_dim(-1)
        layer = Linear(layer_input_dim, layer_output_dim)
        self.layers.append(layer)

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [
            cli.Arg("hidden_dim",   type=int, default=100),
            cli.Arg("depth",        type=int, default=3),
        ]

class ReluMlpLayer(Model):
    def __init__(
        self,
        input_dim:  int,
        output_dim: int,
    ):
        self._torch_module_init()
        self.linear = Linear(input_dim, output_dim)

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.linear.forward(x)
        x = torch.relu(x)
        return x
