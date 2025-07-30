import torch
from jutility import cli, plotting
from juml.commands.base import Command
from juml.train.base import Trainer

class Plot1dRegression(Command):
    @classmethod
    def run(
        cls,
        args:   cli.ParsedArgs,
        n_plot: int,
    ):
        model_dir, model, dataset = Trainer.load(args)

        data = dict()
        xlim = []
        for split in ["train", "test"]:
            data_split  = dataset.get_data_split(split)
            data_loader = dataset.get_data_loader(split, len(data_split))
            x, t = next(iter(data_loader))
            assert isinstance(x, torch.Tensor)
            assert isinstance(t, torch.Tensor)
            data[split] = [x.flatten(), t.flatten()]
            xlim.extend([x.min().item(), x.max().item()])

        x = torch.linspace(min(xlim), max(xlim), n_plot).reshape(n_plot, 1)
        y = model.forward(x).detach().reshape(n_plot)

        mp = plotting.MultiPlot(
            plotting.Subplot(
                plotting.Scatter(*data["train"], c="b", label="train"),
                plotting.Scatter(*data["test" ], c="r", label="test" ),
                plotting.Line(x, y, c="g", label="Prediction"),
                plotting.Legend(),
            ),
            figsize=[8, 6],
            title="%r\n%r" % (model, dataset),
            title_font_size=15,
        )
        mp.save("Predictions", model_dir)

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [
            cli.Arg("n_plot", type=int, default=200),
        ]
