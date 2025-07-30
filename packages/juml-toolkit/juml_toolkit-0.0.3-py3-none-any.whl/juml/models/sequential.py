import torch
from jutility import util, cli, units
from juml.models import embed, pool
from juml.models.base  import Model
from juml.models.embed import Embedder
from juml.models.pool import Pooler

class Sequential(Model):
    def __init__(
        self,
        embedder:   Embedder,
        layer_list: list[Model],
        pooler:     Pooler,
    ):
        self._init_sequential(embedder, pooler)
        for layer in layer_list:
            self.layers.append(layer)

    def _init_sequential(
        self,
        embedder:   Embedder,
        pooler:     Pooler,
    ):
        self._torch_module_init()
        self.embed  = embedder
        self.layers = torch.nn.ModuleList()
        self.pool   = pooler

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.embed.forward(x)

        for layer in self.layers:
            x = layer.forward(x)

        x = self.pool.forward(x)
        return x

    def split(self, layer_ind: int) -> tuple["Sequential", "Sequential"]:
        prefix = Sequential(
            self.embed,
            self.layers[:layer_ind],
            pool.Identity(),
        )
        suffix = Sequential(
            embed.Identity(),
            self.layers[layer_ind:],
            self.pool,
        )
        return prefix, suffix

    @classmethod
    def get_cli_arg(cls):
        return cli.ObjectArg(
            cls,
            *cls.get_cli_options(),
            embed.get_cli_choice(),
            pool.get_cli_choice(),
            tag=cls.get_tag(),
        )

    def __len__(self) -> int:
        return len(self.layers)
