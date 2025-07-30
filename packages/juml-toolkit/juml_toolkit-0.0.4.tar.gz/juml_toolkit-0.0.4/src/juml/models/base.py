import torch
from jutility import util, cli, units

class Model(torch.nn.Module):
    def _torch_module_init(self):
        super().__init__()

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError()

    def init_batch(
        self,
        x: torch.Tensor,
        t: (torch.Tensor | None),
        **kwargs,
    ):
        return

    def num_params(self) -> int:
        return sum(
            int(p.numel())
            for p in self.parameters()
            if  p.requires_grad
        )

    @classmethod
    def get_cli_arg(cls):
        return cli.ObjectArg(
            cls,
            *cls.get_cli_options(),
            tag=cls.get_tag(),
        )

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        raise NotImplementedError()

    @classmethod
    def get_tag(cls) -> (str | None):
        return None

    def __repr__(self):
        return util.format_type(
            type(self),
            num_params=units.metric.format(self.num_params()),
            item_fmt="%s=%s",
        )
