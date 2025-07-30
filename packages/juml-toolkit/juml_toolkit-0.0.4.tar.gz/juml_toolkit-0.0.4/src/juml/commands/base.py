from jutility import cli

class Command(cli.SubCommand):
    @classmethod
    def run(
        cls,
        args: cli.ParsedArgs,
        **kwargs,
    ):
        raise NotImplementedError()

    @classmethod
    def init_juml(cls, train_args: list[cli.Arg]):
        return cls(
            cls.get_name(),
            *[
                arg
                for arg in train_args
                if  cls.include_arg(arg)
            ],
            cli.ArgGroup(
                cls.get_name(),
                *cls.get_cli_options(),
            ),
        )

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__.lower()

    @classmethod
    def include_arg(cls, arg: cli.Arg) -> bool:
        return True

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return []

    def __repr__(self) -> str:
        return self.get_name()
