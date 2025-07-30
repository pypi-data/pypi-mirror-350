from jutility import cli, util
from juml.commands.base import Command
from juml.commands.compare_sweeps import CompareSweeps
from juml.tools.sweeper import Sweeper

class Sweep2d(Command):
    @classmethod
    def run(
        cls,
        args:   cli.ParsedArgs,
        name_1: str,
        name_2: str,
        vals_1: list,
        vals_2: list,
        log_x:  list[str],
        **kwargs,
    ):
        kwargs["log_x"] = log_x
        printer = util.Printer()
        printer.heading("Sweep2d: Sweep all")
        Sweeper(
            args=args,
            **kwargs,
            **args.get_kwargs(),
            params={
                name_1: vals_1,
                name_2: vals_2,
            },
        )
        kwargs["no_cache"] = False
        printer.heading("Sweep2d: Sweep %s" % name_1)
        sweep_configs_1 = cls.sweep_1d_loop(
            args=args,
            name_sweep=name_1,
            vals_sweep=vals_1,
            name_loop=name_2,
            vals_loop=vals_2,
            kwargs=kwargs,
        )
        printer.heading("Sweep2d: Sweep %s" % name_2)
        sweep_configs_2 = cls.sweep_1d_loop(
            args=args,
            name_sweep=name_2,
            vals_sweep=vals_2,
            name_loop=name_1,
            vals_loop=vals_1,
            kwargs=kwargs,
        )
        printer.heading("Sweep2d: Display %s" % name_1)
        CompareSweeps.run(
            args=args,
            config=sweep_configs_1,
            xlabel=name_1,
            clabel=name_2,
            log_x=(name_1 in log_x),
        )
        printer.heading("Sweep2d: Display %s" % name_2)
        CompareSweeps.run(
            args=args,
            config=sweep_configs_2,
            xlabel=name_2,
            clabel=name_1,
            log_x=(name_2 in log_x),
        )

    @classmethod
    def sweep_1d_loop(
        cls,
        args:       cli.ParsedArgs,
        name_sweep: str,
        vals_sweep: list,
        name_loop:  str,
        vals_loop:  list,
        kwargs:     dict,
    ) -> list[dict[str, str]]:
        sweep_configs = []
        for v in vals_loop:
            args.update({name_loop: v})
            sweep = Sweeper(
                args=args,
                **kwargs,
                **args.get_kwargs(),
                params={name_sweep: vals_sweep},
            )
            sweep_configs.append(
                {
                    "series_name":  v,
                    "sweep_name":   sweep.name,
                    "param_name":   name_sweep,
                },
            )

        return sweep_configs

    @classmethod
    def include_arg(cls, arg: cli.Arg) -> bool:
        return True if (arg.name != "devices") else False

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [
            cli.Arg("name_1",       type=str,   required=True),
            cli.Arg("name_2",       type=str,   required=True),
            cli.JsonArg("vals_1",   nargs="*",  required=True),
            cli.JsonArg("vals_2",   nargs="*",  required=True),
            *[
                arg
                for arg in Sweeper.get_cli_options()
                if  arg.name != "params"
            ],
        ]
