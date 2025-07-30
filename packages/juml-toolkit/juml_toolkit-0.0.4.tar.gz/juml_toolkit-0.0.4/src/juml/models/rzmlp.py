import torch
from jutility import cli
from juml.models.base import Model
from juml.models.sequential import Sequential
from juml.models.embed import Embedder
from juml.models.pool import Pooler
from juml.models.linear import Linear

class RzMlp(Sequential):
    def __init__(
        self,
        input_shape:    list[int],
        output_shape:   list[int],
        model_dim:      int,
        expand_ratio:   float,
        depth:          int,
        embedder:       Embedder,
        pooler:         Pooler,
    ):
        self._init_sequential(embedder, pooler)
        self.embed.set_input_shape(input_shape)
        self.pool.set_shapes([model_dim], output_shape)

        layer = Linear(self.embed.get_output_dim(-1), model_dim)
        self.layers.append(layer)

        for _ in range(depth):
            layer = ReZeroMlpLayer(model_dim, expand_ratio)
            self.layers.append(layer)

        layer = Linear(model_dim, self.pool.get_input_dim(-1))
        self.layers.append(layer)

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [
            cli.Arg("model_dim",    type=int,   default=100),
            cli.Arg("expand_ratio", type=float, default=2.0, tag="x"),
            cli.Arg("depth",        type=int,   default=3),
        ]

class ReZeroMlpLayer(Model):
    def __init__(
        self,
        model_dim:      int,
        expand_ratio:   float,
    ):
        self._torch_module_init()
        hidden_dim  = int(model_dim * expand_ratio)
        self.f1     = Linear(model_dim, hidden_dim)
        self.f2     = Linear(hidden_dim, model_dim)
        self.scale  = torch.nn.Parameter(torch.tensor(0.0))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x_res = self.f1.forward(x)
        x_res = torch.relu(x_res)
        x_res = self.f2.forward(x_res)
        x = x + (self.scale * x_res)
        return x
