import os
import multiprocessing
import queue
from jutility import plotting, util, cli
from juml.train.base import Trainer
from juml.tools.experiment import ExperimentGroup

class Sweeper:
    def __init__(
        self,
        args:       cli.ParsedArgs,
        params:     dict[str, list],
        devices:    list[list[int]],
        seeds:      list[int],
        no_cache:   bool,
        log_x:      list[str],
        configs:    list[str],
        **train_kwargs,
    ):
        printer = util.Printer()
        printer.heading("Sweeper: Initialise experiments")

        Trainer.apply_configs(args, configs, list(params.keys()))
        self.params         = params
        self.seeds          = seeds
        self.log_x          = log_x
        self.experiments    = ExperimentGroup.from_params(params, seeds)
        self.init_metric_info(args)
        self.init_name(args)
        self.init_output_dir()

        printer.heading("Sweeper: Run experiments")

        if len(devices) == 1:
            [d] = devices
            cli.verbose.reset()
            self.run_single_process(
                args=args,
                devices=d,
                no_cache=no_cache,
                train_kwargs=train_kwargs,
                printer=printer,
            )
        else:
            self.run_multi_process(
                args=args,
                devices=devices,
                no_cache=no_cache,
                train_kwargs=train_kwargs,
            )

        printer.heading("Sweeper: display results")

        self.experiments.load_results(args, self.opt_str)
        self.best = (
            max(self.experiments)
            if self.maximise else
            min(self.experiments)
        )

        self.best_model_dir = self.best.metrics["model_dir"]
        self.plot_paths = [os.path.join(self.best_model_dir, "metrics.png")]

        for param_name in self.params.keys():
            self.plot_param(param_name)

        self.save_results_markdown()
        self.experiments.save(self.output_dir)

    def init_metric_info(self, args: cli.ParsedArgs):
        dataset = Trainer.init_dataset(args)
        loss    = Trainer.init_loss(args, dataset)
        self.metric_info    = loss.metric_info()
        self.maximise       = loss.metric_higher_is_better()
        self.opt_str        = "max" if self.maximise else "min"

    def init_name(self, args: cli.ParsedArgs):
        original_args = {k: args.get_value(k) for k in self.params.keys()}
        original_args["seed"] = args.get_value("seed")

        for i, e in enumerate(self.experiments, start=1):
            print("(%2i) %s" % (i, e.arg_str))
            args.update(e.arg_dict)
            e.set_model_name(Trainer.get_summary(args))
            e.set_ind(i)

        args.update(original_args)
        sorted_names = sorted(e.model_name for e in self.experiments)
        self.name = util.merge_strings(sorted_names)

    def init_output_dir(self):
        self.output_dir = os.path.join("results", "sweep", self.name)

    def run_single_process(
        self,
        args:           cli.ParsedArgs,
        devices:        list[int],
        no_cache:       bool,
        train_kwargs:   dict,
        printer:        util.Printer,
    ):
        for e in self.experiments:
            run_experiment(
                args=args,
                devices=devices,
                no_cache=no_cache,
                train_kwargs=train_kwargs,
                args_update_dict=e.arg_dict,
                printer=printer,
            )

    def run_multi_process(
        self,
        args:           cli.ParsedArgs,
        devices:        list[list[int]],
        no_cache:       bool,
        train_kwargs:   dict,
    ):
        mp_context = multiprocessing.get_context("spawn")

        q = mp_context.Queue()
        for e in self.experiments:
            q.put(e.arg_dict)

        p_list = [
            mp_context.Process(
                target=sweeper_subprocess,
                kwargs={
                    "args":         args,
                    "q":            q,
                    "pid":          i,
                    "devices":      d,
                    "no_cache":     no_cache,
                    "train_kwargs": train_kwargs,
                    "output_dir":   self.output_dir,
                },
            )
            for i, d in enumerate(devices)
        ]

        for p in p_list:
            p.start()

        for p in p_list:
            p.join()

    def plot_param(self, param_name: str):
        sweep = self.experiments.sweep_param(self.best, param_name)

        x_index = not sweep.is_numeric()
        log_x = (True if (param_name in self.log_x) else False)
        log_y = self.metric_info.get("log_y", False)
        results_train   = plotting.NoisyData(log_y=log_y, x_index=x_index)
        results_test    = plotting.NoisyData(log_y=log_y, x_index=x_index)
        results_time    = plotting.NoisyData(log_y=True,  x_index=x_index)
        results_size    = plotting.NoisyData(log_y=True,  x_index=x_index)

        for e in sweep:
            val = e.arg_dict[param_name]
            results_train.update(val,   e.metrics["train"][self.opt_str])
            results_test.update(val,    e.metrics["test" ][self.opt_str])
            results_time.update(val,    e.metrics["time" ])
            results_size.update(val,    e.metrics["num_params"])

        mp = plotting.MultiPlot(
            plotting.Subplot(
                results_train.plot(),
                results_train.plot_best(
                    maximise=self.maximise,
                    label_fmt="(%s, %.5f)",
                ),
                plotting.Legend(),
                **results_train.get_xtick_kwargs(),
                **self.metric_info,
                xlabel=param_name,
                log_x=log_x,
                title="Best train metric",
            ),
            plotting.Subplot(
                results_test.plot(),
                results_test.plot_best(
                    maximise=self.maximise,
                    label_fmt="(%s, %.5f)",
                ),
                plotting.Legend(),
                **results_test.get_xtick_kwargs(),
                **self.metric_info,
                xlabel=param_name,
                log_x=log_x,
                title="Best test metric",
            ),
            plotting.Subplot(
                results_time.plot(),
                **results_time.get_xtick_kwargs(),
                xlabel=param_name,
                log_x=log_x,
                log_y=True,
                ylabel="Time (s)",
                title="Training duration",
            ),
            plotting.Subplot(
                results_size.plot(),
                **results_size.get_xtick_kwargs(),
                xlabel=param_name,
                log_x=log_x,
                log_y=True,
                ylabel="Number of parameters",
                title="Model size",
            ),
            title="%s\n%r" % (param_name, self.params[param_name]),
            title_font_size=15,
            figsize=[10, 8],
        )
        full_path = mp.save(param_name, self.output_dir)
        self.plot_paths.append(full_path)

    def save_results_markdown(self):
        md = util.MarkdownPrinter("results", self.output_dir)
        md.title("Sweep results")

        md.heading("Summary", end="\n\n")
        table = util.Table.key_value(printer=md)
        table.update(k="`#` experiments",   v=len(self.experiments))
        table.update(k="Best result",       v="%.5f" % self.best.result)
        table.update(k="Target metric",     v="`test.%s`" % self.opt_str)
        for param_name, param_vals in self.params.items():
            table.update(k=md.code(param_name), v=md.code(str(param_vals)))

        table.update(k="`seeds`", v=md.code(str(self.seeds)))

        md.heading("Best model")
        best_rel_dir = os.path.relpath(self.best_model_dir, self.output_dir)
        best_args_json      = os.path.join(best_rel_dir, "args.json")
        best_metrics_json   = os.path.join(best_rel_dir, "metrics.json")
        md.file_link(best_args_json,    "Best args (JSON)")
        md.file_link(best_metrics_json, "Best metrics (JSON)", end="\n\n")
        table = util.Table.key_value(printer=md)
        table.update(k="Params/seed",  v=md.code(self.best.arg_str))

        for name, metric in [
            ("Model",               "repr_model"),
            ("Model name",          "model_name"),
            ("Train metrics",       "train_summary"),
            ("Test metrics",        "test_summary"),
            ("Training duration",   "time_str"),
            ("`#` parameters",      "num_params"),
        ]:
            table.update(k=name, v=md.code(self.best.metrics[metric]))

        for name, val in self.best.arg_dict.items():
            table.update(k="`--%s`" % name, v=md.code(val))

        md.heading("Statistics", end="\n\n")
        table = util.Table.key_value(md)
        best_config_sweep = self.experiments.sweep_seeds(self.best)
        mean_best = best_config_sweep.results_mean()
        mean_all = self.experiments.results_mean()
        table.update(k="Mean (best params)",    v="%.5f" % mean_best)
        table.update(k="Mean (all)",            v="%.5f" % mean_all)

        if len(self.seeds) >= 2:
            std_best = best_config_sweep.results_std()
            std_all = self.experiments.results_std()
            table.update(k="STD (best params)", v="%.5f" % std_best)
            table.update(k="STD (all)",         v="%.5f" % std_all)

        md.heading("Metrics")
        for full_path in self.plot_paths:
            md.image(os.path.relpath(full_path, self.output_dir))

        md.heading("All results", end="\n\n")
        table = util.Table(
            util.Column("rank",     "i",    width=-10),
            util.Column("result",   ".5f",  title="`test.%s`" % self.opt_str),
            *[
                util.Column(param_name, title=md.code(param_name))
                for param_name in self.params.keys()
            ],
            util.Column("seed", "i", title="`seed`"),
            util.Column("model_name"),
            printer=md,
        )
        sorted_experiments = sorted(self.experiments, reverse=self.maximise)
        for i, e in enumerate(sorted_experiments, start=1):
            metrics_png = os.path.join(e.metrics["model_dir"], "metrics.png")
            metrics_rel = os.path.relpath(metrics_png, self.output_dir)
            table.update(
                rank=i,
                result=e.result,
                model_name="[`%s`](%s)" % (e.model_name, metrics_rel),
                **e.arg_dict,
            )

        md.git_add(
            md.get_filename(),
            os.path.join(self.best_model_dir, "args.json"),
            os.path.join(self.best_model_dir, "metrics.json"),
            *self.plot_paths,
        )
        md.readme_include("`[ full_sweep_results ]`", *self.plot_paths)
        md.show_command("sweep")
        md.flush()

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [
            cli.JsonArg(
                "params",
                default=dict(),
                metavar=": dict[str, list] = \"{}\"",
                help=(
                    "EG '{\"trainer.BpSp.epochs\":[100,200,300],"
                    "\"trainer.BpSp.optimiser.Adam.lr\":"
                    "[1e-5,1e-4,1e-3,1e-2]}'"
                )
            ),
            cli.JsonArg(
                "devices",
                default=[[]],
                metavar=": list[list[int]] = \"[[]]\"",
                help="EG \"[[1,2,3],[3,4],[5]]\" or \"[[],[],[],[],[],[]]\""
            ),
            cli.Arg(
                "seeds",
                type=int,
                nargs="+",
                default=list(range(5)),
            ),
            cli.Arg("no_cache", action="store_true"),
            cli.Arg("log_x",    type=str, default=[], nargs="+"),
        ]

def sweeper_subprocess(
    args:           cli.ParsedArgs,
    q:              multiprocessing.Queue,
    pid:            int,
    devices:        list[int],
    no_cache:       bool,
    train_kwargs:   dict,
    output_dir:     str,
):
    printer = util.Printer(
        "p%i_log" % pid,
        dir_name=output_dir,
        print_to_console=False,
    )
    printer("Devices = %s" % devices)
    while True:
        try:
            args_update_dict = q.get(block=False)
        except queue.Empty:
            return

        run_experiment(
            args=args,
            devices=devices,
            no_cache=no_cache,
            train_kwargs=train_kwargs,
            args_update_dict=args_update_dict,
            printer=printer,
        )

def run_experiment(
    args:               cli.ParsedArgs,
    devices:            list[int],
    no_cache:           bool,
    train_kwargs:       dict,
    args_update_dict:   dict,
    printer:            util.Printer,
):
    args.update(args_update_dict)
    for key in args_update_dict:
        if key in train_kwargs:
            train_kwargs[key] = args_update_dict[key]

    metrics_path = Trainer.get_metrics_path(args)
    if (not os.path.isfile(metrics_path)) or no_cache:
        with util.Timer(
            name=str(args_update_dict),
            printer=printer,
            hline=True,
        ):
            Trainer.from_args(
                args,
                devices=devices,
                configs=[],
                printer=printer,
                **train_kwargs,
            )
    else:
        print("Found cached results `%s` -> skip" % metrics_path)
