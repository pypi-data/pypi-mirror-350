from jutility import cli
from juml.commands.base import Command
from juml.train.base import Trainer
from juml.tools.profiler import Profiler

class Profile(Command):
    @classmethod
    def run(
        cls,
        args:           cli.ParsedArgs,
        batch_size:     int,
        num_warmup:     int,
        num_profile:    int,
        devices:        list[int],
        sort_by:        str,
    ):
        model_dir, model, dataset = Trainer.load(args)
        return Profiler(
            model=model,
            dataset=dataset,
            model_dir=model_dir,
            batch_size=batch_size,
            num_warmup=num_warmup,
            num_profile=num_profile,
            devices=devices,
            name="profile",
            sort_by=sort_by,
        )

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [
            cli.Arg("batch_size",   type=int, default=100),
            cli.Arg("num_warmup",   type=int, default=10),
            cli.Arg("num_profile",  type=int, default=10),
            cli.Arg("devices",      type=int, default=[], nargs="*"),
            cli.Arg("sort_by",      type=str, default="self_cpu_time_total"),
        ]
