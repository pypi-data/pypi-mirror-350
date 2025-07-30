import os
from jutility import cli, util
from juml.commands.base import Command
from juml.device import DeviceConfig
from juml.train.base import Trainer
from juml.tools.display import plot_sequential

class PlotSequential(Command):
    @classmethod
    def run(
        cls,
        args:           cli.ParsedArgs,
        batch_size:     int,
        num_warmup:     int,
        devices:        list[int],
    ):
        device_cfg = DeviceConfig(devices)
        model_dir, model, dataset = Trainer.load(args)
        device_cfg.set_module_device(model)

        train_loader = dataset.get_data_loader("train", batch_size)
        x, t = next(iter(train_loader))
        [x] = device_cfg.to_device([x])

        for _ in range(num_warmup):
            y = model.forward(x)

        name = cls.get_name()
        md = util.MarkdownPrinter(name, model_dir)
        md.title(md.code(repr(model)), end="\n\n")
        md.set_print_to_console(True)

        mp = plot_sequential(model, x, md)
        mp.save(name, model_dir)

        md.set_print_to_console(False)
        md.image(name + ".png")

        md.git_add(md.get_filename(), mp.full_path)
        md.readme_include("`[ %s ]`" % repr(model))
        md.show_command("plotsequential")
        md.flush()

        return mp

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [
            cli.Arg("batch_size",   type=int, default=100),
            cli.Arg("num_warmup",   type=int, default=10),
            cli.Arg("devices",      type=int, default=[], nargs="*"),
        ]
