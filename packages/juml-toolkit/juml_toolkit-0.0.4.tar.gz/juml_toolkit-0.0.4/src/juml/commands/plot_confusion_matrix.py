import torch
from jutility import cli, plotting
from juml.commands.base import Command
from juml.train.base import Trainer

class PlotConfusionMatrix(Command):
    @classmethod
    def run(
        cls,
        args: cli.ParsedArgs,
    ):
        model_dir, model, dataset = Trainer.load(args)

        test_split  = dataset.get_data_split("test")
        test_loader = dataset.get_data_loader("test", len(test_split))
        x, t = next(iter(test_loader))
        y = model.forward(x).argmax(dim=-1)

        c = torch.zeros([10, 10])
        for ground_truth in range(10):
            for prediction in range(10):
                n = (y[t == ground_truth] == prediction).sum()
                c[prediction, ground_truth] = n

        mp = plotting.MultiPlot(
            plotting.Subplot(
                plotting.ColourMesh(c),
                xlabel="Ground truth",
                ylabel="Prediction",
                axis_square=True,
            ),
            plotting.ColourBar(
                c.min(),
                c.max(),
                label="Number of classifications",
            ),
            width_ratios=[1, 0.1],
            figsize=[6, 5],
            title="Confusion matrix\n%r\n%r" % (model, dataset),
            title_font_size=15,
        )
        mp.save("Confusion matrix", model_dir)
