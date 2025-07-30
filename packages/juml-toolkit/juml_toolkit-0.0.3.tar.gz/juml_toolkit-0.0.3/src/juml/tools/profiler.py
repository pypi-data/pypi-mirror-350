import torch
from torch.autograd.profiler_util import FunctionEventAvg
from jutility import util, units
from juml.models.base import Model
from juml.datasets.base import Dataset
from juml.device import DeviceConfig
from juml.train.base import Trainer

class Profiler:
    def __init__(
        self,
        model:          Model,
        dataset:        Dataset,
        model_dir:      (str | None),
        batch_size:     int,
        num_warmup:     int,
        num_profile:    int,
        devices:        list[int],
        name:           str,
        sort_by:        str,
    ):
        device_cfg = DeviceConfig(devices)
        device_cfg.set_module_device(model)

        train_loader = dataset.get_data_loader("train", batch_size)
        x, t = next(iter(train_loader))
        [x] = device_cfg.to_device([x])

        for _ in range(num_warmup):
            y = model.forward(x)

        activities = [torch.profiler.ProfilerActivity.CPU]
        if len(devices) > 0:
            activities.append(torch.profiler.ProfilerActivity.CUDA)

        profiler_kwargs = {
            "activities":       activities,
            "profile_memory":   True,
            "with_flops":       True,
        }
        with torch.profiler.profile(**profiler_kwargs) as prof:
            with torch.profiler.record_function("model.forward"):
                for _ in range(num_profile):
                    y = model.forward(x)

        self.ka = prof.key_averages()
        printer = util.Printer(name, dir_name=model_dir)
        printer(self.ka.table(sort_by=sort_by))

        self.cpu_total  = self.get_cpu_total(self.ka)
        self.cuda_total = self.get_cuda_total(self.ka)
        self.t_total    = self.cpu_total + self.cuda_total
        self.n_samples  = batch_size * num_profile
        self.t_sample   = self.t_total / self.n_samples
        self.throughput = 1 / self.t_sample
        self.flops      = self.get_flops_total(self.ka) / self.n_samples
        profile_dict    = {
            "t_total":          self.t_total,
            "t_sample":         self.t_sample,
            "throughput":       self.throughput,
            "flops":            self.flops,
            "n_samples":        self.n_samples,
            "n_samples_str":    units.metric.format(self.n_samples),
            "batch_size":       batch_size,
            "n_repeats":        num_profile,
            "t_total_str": (
                "%.5f s"
                % self.t_total
            ),
            "t_sample_str": (
                "%.5f ms/sample"
                % (self.t_sample * 1e3)
            ),
            "throughput_str": (
                "%s samples/second"
                % units.metric.format(self.throughput)
            ),
            "flops_str": (
                "%s FLOPS/sample"
                % units.metric.format(self.flops).upper()
            ),
        }
        util.save_json(profile_dict, name, model_dir)

        md = util.MarkdownPrinter(name, model_dir)
        table = util.Table.key_value(printer=md)
        table.update(k="Model", v="`%s`" % repr(model))
        for name, dict_key in [
            ("Time (total)",    "t_total_str"),
            ("Time (average)",  "t_sample_str"),
            ("Throughput",      "throughput_str"),
            ("FLOPS",           "flops_str"),
            ("Total #samples",  "n_samples_str"),
            ("Batch size",      "batch_size"),
            ("`#`repeats",      "n_repeats"),
        ]:
            table.update(k=name, v=profile_dict[dict_key])

    @classmethod
    def get_cpu_total(cls, event_list: list[FunctionEventAvg]) -> float:
        return sum(e.self_cpu_time_total for e in event_list) * 1e-6

    @classmethod
    def get_cuda_total(cls, event_list: list[FunctionEventAvg]) -> float:
        return sum(e.self_cuda_time_total for e in event_list) * 1e-6

    @classmethod
    def get_flops_total(cls, event_list: list[FunctionEventAvg]) -> float:
        return sum(e.flops for e in event_list)
