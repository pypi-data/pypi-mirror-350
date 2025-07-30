from jutility import cli, util
from juml import models, datasets, loss, train, commands
from juml.models.base import Model
from juml.datasets.base import Dataset
from juml.loss.base import Loss
from juml.train.base import Trainer
from juml.commands.base import Command

class Framework:
    @classmethod
    def get_models(cls) -> list[type[Model]]:
        return models.get_all()

    @classmethod
    def get_datasets(cls) -> list[type[Dataset]]:
        return datasets.get_all()

    @classmethod
    def get_losses(cls) -> list[type[Loss]]:
        return loss.get_all()

    @classmethod
    def get_trainers(cls) -> list[type[Trainer]]:
        return train.get_all()

    @classmethod
    def get_commands(cls) -> list[type[Command]]:
        return commands.get_all()

    @classmethod
    def get_defaults(cls) -> dict[str, str | None]:
        return {
            "model":    None,
            "dataset":  None,
            "loss":     None,
            "trainer":  "BpSp",
        }

    @classmethod
    def get_train_args(cls) -> list[cli.Arg]:
        defaults = cls.get_defaults()
        return [
            cli.ObjectChoice(
                "loss",
                *[t.get_cli_arg() for t in cls.get_losses()],
                default=defaults["loss"],
                is_group=True,
                required=False,
            ),
            cli.ObjectChoice(
                "dataset",
                *[t.get_cli_arg() for t in cls.get_datasets()],
                default=defaults["dataset"],
                is_group=True,
            ),
            cli.ObjectChoice(
                "model",
                *[t.get_cli_arg() for t in cls.get_models()],
                default=defaults["model"],
                is_group=True,
            ),
            cli.ObjectChoice(
                "trainer",
                *[t.get_cli_arg() for t in cls.get_trainers()],
                default=defaults["trainer"],
                is_group=True,
            ),
            cli.Arg("seed",         type=int, default=0),
            cli.Arg("devices",      type=int, default=[],   nargs="*"),
            cli.Arg("configs",      type=str, default=[],   nargs="*"),
            cli.Arg("model_name",   type=str, default=None, is_kwarg=False),
            cli.Arg("print_level",  type=int, default=0),
        ]

    @classmethod
    def get_parser(cls) -> cli.Parser:
        return cli.Parser(
            sub_commands=cli.SubCommandGroup(
                *[
                    command_type.init_juml(cls.get_train_args())
                    for command_type in cls.get_commands()
                ],
            ),
        )

    @classmethod
    def run(cls, *parser_args, **parser_kwargs):
        parser  = cls.get_parser()
        args    = parser.parse_args(*parser_args, **parser_kwargs)
        command = args.get_command()
        kwargs  = args.get_arg(command.name).get_kwargs()

        with util.Timer(repr(command)):
            command.run(args, **kwargs)
