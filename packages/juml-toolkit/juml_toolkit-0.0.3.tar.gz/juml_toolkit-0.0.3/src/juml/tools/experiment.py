import os
import statistics
from jutility import util, cli
from juml.train.base import Trainer

class Experiment:
    def __init__(
        self,
        arg_dict:   dict,
        model_name: (str    | None),
        ind:        (int    | None),
        metrics:    (dict   | None),
        result:     (float  | None),
    ):
        self.arg_dict   = arg_dict
        self.arg_str    = util.format_dict(arg_dict)
        self.model_name = model_name
        self.ind        = ind
        self.metrics    = metrics
        self.result     = result

    @classmethod
    def from_arg_dict(cls, arg_dict: dict):
        return cls(
            arg_dict=arg_dict,
            model_name=None,
            ind=None,
            metrics=None,
            result=None,
        )

    def to_dict(self) -> dict:
        return {
            "arg_dict":     self.arg_dict,
            "model_name":   self.model_name,
            "ind":          self.ind,
            "metrics":      self.metrics,
            "result":       self.result,
        }

    def set_model_name(self, model_name: str):
        self.model_name = model_name

    def set_ind(self, ind: int):
        self.ind = ind

    def load_result(self, args: cli.ParsedArgs, key: str):
        if self.result is not None:
            raise ValueError(
                "%r already has result=%s"
                % (self, self.result)
            )

        args.update(self.arg_dict)
        self.metrics    = util.load_json(Trainer.get_metrics_path(args))
        self.result     = self.metrics["test"][key]

        if not isinstance(self.result, float):
            raise ValueError(
                "metrics['test'][%r] = %s has type `%s`, expected `float`"
                % (key, self.result, type(self.result).__name__)
            )

    def __repr__(self) -> str:
        return util.format_type(type(self), **self.arg_dict)

    def __lt__(self, other: "Experiment") -> bool:
        return (self.result < other.result)

class ExperimentGroup:
    def __init__(
        self,
        params:         dict[str, list],
        seeds:          list[int],
        experiments:    list[Experiment],
    ):
        self.params             = params
        self.seeds              = seeds
        self.experiment_list    = experiments
        self.experiment_dict    = {e.arg_str: e for e in experiments}

    @classmethod
    def from_params(
        cls,
        params: dict[str, list],
        seeds:  list[int],
    ):
        components_list = [[["seed", s]] for s in seeds]
        for param_name, param_vals in params.items():
            components_list = [
                c + p
                for c in components_list
                for p in [[[param_name, v]] for v in param_vals]
            ]

        return cls(
            params=params,
            seeds=seeds,
            experiments=[
                Experiment.from_arg_dict({k: v for k, v in c})
                for c in components_list
            ],
        )

    @classmethod
    def load(cls, sweep_name: str):
        dir_name    = os.path.join("results", "sweep", sweep_name)
        full_path   = util.get_full_path(
            "experiments.json",
            dir_name=dir_name,
            loading=True,
        )
        eg_dict = util.load_json(full_path)
        return cls(
            params=eg_dict["params"],
            seeds=eg_dict["seeds"],
            experiments=[
                Experiment(**ed)
                for ed in eg_dict["experiments"]
            ],
        )

    def save(self, output_dir: str):
        util.save_json(
            {
                "params":       self.params,
                "seeds":        self.seeds,
                "experiments":  [e.to_dict() for e in self.experiment_list],
            },
            "experiments",
            dir_name=output_dir,
        )

    def load_results(self, args: cli.ParsedArgs, key: str):
        for e in self.experiment_list:
            e.load_result(args, key)

    def sweep_seeds(
        self,
        root_experiment: Experiment,
    ) -> "ExperimentGroup":
        experiment_list = []
        root_dict       = root_experiment.arg_dict
        root_seed       = root_dict["seed"]

        for seed in self.seeds:
            root_dict["seed"] = seed
            arg_str = util.format_dict(root_dict)
            experiment_list.append(self.experiment_dict[arg_str])

        root_dict["seed"] = root_seed
        return ExperimentGroup(
            params=dict(),
            seeds=self.seeds,
            experiments=experiment_list,
        )

    def sweep_param(
        self,
        root_experiment:    Experiment,
        param_name:         str,
    ) -> "ExperimentGroup":
        experiment_list = []
        root_dict       = root_experiment.arg_dict
        root_val        = root_dict[param_name]
        root_seed       = root_dict["seed"]

        for val in self.params[param_name]:
            for seed in self.seeds:
                root_dict[param_name]   = val
                root_dict["seed"]       = seed
                arg_str = util.format_dict(root_dict)
                experiment_list.append(self.experiment_dict[arg_str])

        root_dict[param_name]   = root_val
        root_dict["seed"]       = root_seed
        return ExperimentGroup(
            params={param_name: self.params[param_name]},
            seeds=self.seeds,
            experiments=experiment_list,
        )

    def is_numeric(self) -> bool:
        return all(
            (isinstance(v, int) or isinstance(v, float))
            for param_vals in self.params.values()
            for v in param_vals
        )

    def get_results(self) -> list[float | None]:
        return [e.result for e in self.experiment_list]

    def results_mean(self) -> float:
        return statistics.mean(self.get_results())

    def results_std(self) -> float:
        return statistics.stdev(self.get_results())

    def __iter__(self):
        return iter(self.experiment_list)

    def __len__(self):
        return len(self.experiment_list)
