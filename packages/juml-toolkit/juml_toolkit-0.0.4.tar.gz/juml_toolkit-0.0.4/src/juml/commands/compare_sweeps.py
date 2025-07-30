import os
from jutility import cli, util, plotting
from juml.commands.base import Command
from juml.datasets.base import Dataset
from juml.loss.base import Loss
from juml.tools.experiment import Experiment, ExperimentGroup
from juml.tools.plot_type import PlotType

class CompareSweeps(Command):
    @classmethod
    def run(
        cls,
        args:       cli.ParsedArgs,
        config:     list[dict[str, str]],
        xlabel:     str,
        clabel:     str,
        name:       (str | None),
        log_x:      bool,
        plot_type:  PlotType,
    ):
        dataset_type = args.get_type("dataset")
        assert issubclass(dataset_type, Dataset)

        loss_arg = args.get_arg("loss")
        loss_arg.set_default_choice(dataset_type.get_default_loss())
        loss_type = args.get_type("loss")
        assert issubclass(loss_type, Loss)

        metric_info = loss_type.metric_info()
        maximise    = loss_type.metric_higher_is_better()
        log_y       = metric_info.get("log_y", False)
        opt_str     = "max" if maximise else "min"
        cp          = plotting.ColourPicker(len(config), cyclic=False)

        series = [
            SweepSeries(
                **c,
                maximise=maximise,
                log_y=log_y,
                opt_str=opt_str,
                colour=cp.next(),
            )
            for c in config
        ]

        if name is None:
            name = util.merge_strings([s.sweep_name for s in series])

        output_dir = os.path.join("results", "compare", name)

        x_index = any((not s.experiments.is_numeric()) for s in series)
        xtick_config = plotting.NoisyData(x_index=x_index)
        for s in series:
            for param_vals in s.experiments.params.values():
                for v in param_vals:
                    xtick_config.update(v, None)

        axis_kwargs = {"xlabel": xlabel, "log_x": log_x}
        axis_kwargs.update(xtick_config.get_xtick_kwargs())

        mp = plotting.MultiPlot(
            plotting.Subplot(
                *[
                    s.plot(x_index, TrainGetter())
                    for s in series
                ],
                **axis_kwargs,
                **metric_info,
                title="Best train metric",
            ),
            plotting.Subplot(
                *[
                    s.plot(x_index, TestGetter())
                    for s in series
                ],
                **axis_kwargs,
                **metric_info,
                title="Best test metric",
            ),
            plotting.Subplot(
                *[
                    s.plot(x_index, TimeGetter())
                    for s in series
                ],
                **axis_kwargs,
                log_y=True,
                ylabel="Time (s)",
                title="Training duration",
            ),
            plotting.Subplot(
                *[
                    s.plot(x_index, SizeGetter())
                    for s in series
                ],
                **axis_kwargs,
                log_y=True,
                ylabel="Number of parameters",
                title="Model size",
            ),
            legend=plotting.FigureLegend(
                *[s.get_legend_plottable() for s in series],
                num_rows=None,
                loc="outside right upper",
                title=clabel,
            ),
            figsize=[10, 8],
        )
        plot_type.plot(mp, xlabel, output_dir)

        md = util.MarkdownPrinter(xlabel, output_dir)
        md.title("Sweep comparison")
        md.heading("Metrics")
        md.image(md.rel_path(mp.full_path))
        md.heading("Sweeps", end="\n\n")
        table = util.Table.key_value(printer=md)
        for s in series:
            table.update(
                k=s.series_name,
                v="[`[ %s ]`](../../sweep/%s/results.md)" % (
                    s.sweep_name,
                    s.sweep_name,
                ),
            )

        md.git_add(
            md.get_filename(),
            mp.full_path,
            *["results/sweep/%s/results.md" % s.sweep_name for s in series],
        )
        md.readme_include("`[ compare_sweeps ]`", mp.full_path)
        md.show_command("comparesweeps")
        md.flush()

        return mp

    @classmethod
    def include_arg(cls, arg: cli.Arg) -> bool:
        return arg.name in ["dataset", "loss"]

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [
            cli.JsonArg(
                "config",
                required=True,
                metavar=": list[dict[\"series_name\": str, "
                "\"sweep_name\": str, \"param_name\": str]]",
                help=(
                    "EG '[{\"series_name\":\"MLP\","
                    "\"sweep_name\":\"mlp_sweep_name_s1,2,3\","
                    "\"param_name\":\"model.RzMlp.depth\"},"
                    "{\"series_name\":\"CNN\","
                    "\"sweep_name\":\"cnn_sweep_name_s1,2,3\","
                    "\"param_name\":\"model.RzCnn.depth\"}]'"
                )
            ),
            cli.Arg("xlabel",   type=str, required=True),
            cli.Arg("clabel",   type=str, required=True),
            cli.Arg("name",     type=str, default=None),
            cli.Arg("log_x",    action="store_true"),
            PlotType.get_cli_arg(),
        ]

class SweepSeries:
    def __init__(
        self,
        series_name:    str,
        sweep_name:     str,
        param_name:     str,
        maximise:       bool,
        log_y:          bool,
        opt_str:        str,
        colour:         list[float],
    ):
        self.series_name    = series_name
        self.sweep_name     = sweep_name
        self.param_name     = param_name
        self.log_y          = log_y
        self.opt_str        = opt_str
        self.colour         = colour

        eg_all              = ExperimentGroup.load(sweep_name)
        best                = max(eg_all) if maximise else min(eg_all)
        self.experiments    = eg_all.sweep_param(best, param_name)

    def plot(self, x_index: bool, mg: "MetricGetter") -> plotting.Plottable:
        nd = plotting.NoisyData(log_y=self.log_y, x_index=x_index)
        for e in self.experiments:
            x = e.arg_dict[self.param_name]
            y = mg.get(e.metrics, self.opt_str)
            nd.update(x, y)

        return nd.plot(c=self.colour)

    def get_legend_plottable(self) -> plotting.Plottable:
        nd = plotting.NoisyData()
        return nd.plot(c=self.colour, label=self.series_name)

class MetricGetter:
    def get(self, metrics: dict, opt_str: str) -> float:
        raise NotImplementedError()

class TrainGetter(MetricGetter):
    def get(self, metrics: dict, opt_str: str) -> float:
        return metrics["train"][opt_str]

class TestGetter(MetricGetter):
    def get(self, metrics: dict, opt_str: str) -> float:
        return metrics["test"][opt_str]

class TimeGetter(MetricGetter):
    def get(self, metrics: dict, opt_str: str) -> float:
        return metrics["time"]

class SizeGetter(MetricGetter):
    def get(self, metrics: dict, opt_str: str) -> float:
        return metrics["num_params"]
