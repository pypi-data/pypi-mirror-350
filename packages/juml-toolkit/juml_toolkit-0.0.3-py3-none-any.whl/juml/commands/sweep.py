from jutility import cli
from juml.commands.base import Command
from juml.tools.sweeper import Sweeper

class Sweep(Command):
    @classmethod
    def run(
        cls,
        args: cli.ParsedArgs,
        **kwargs,
    ):
        return Sweeper(
            args=args,
            **kwargs,
            **args.get_kwargs(),
        )

    @classmethod
    def include_arg(cls, arg: cli.Arg) -> bool:
        return True if (arg.name != "devices") else False

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return Sweeper.get_cli_options()
