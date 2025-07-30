import torch
from jutility import cli, util
from juml.device import DeviceConfig
from juml.train.base import Trainer
from juml.train.bpsp import BpSp
from juml.models.base import Model
from juml.datasets.base import Dataset
from juml.loss.base import Loss

class BpSpDe(Trainer):
    def train(
        self,
        args:       cli.ParsedArgs,
        model:      Model,
        dataset:    Dataset,
        loss:       Loss,
        device_cfg: DeviceConfig,
        table:      util.Table,
        batch_size: int,
        steps:      int,
        n_train:    int,
        optimiser:  torch.optim.Optimizer,
        lrs:        torch.optim.lr_scheduler.LRScheduler,
    ):
        train_loader = dataset.get_subset_loader(
            split="train",
            subset_size=n_train,
            batch_size=batch_size,
        )
        test_loader  = dataset.get_data_loader(
            split="test",
            batch_size=batch_size,
        )

        table.get_column("train_metric").set_callback(
            callback=(lambda: loss.metric(model, train_loader, device_cfg)),
            level=1,
        )
        table.get_column("test_metric").set_callback(
            callback=(lambda: loss.metric(model, test_loader, device_cfg)),
            level=1,
        )

        s = 0
        e = 0
        table.update(level=1, step=s, epoch=e)
        while s < steps:
            for i, (x, t) in enumerate(train_loader):
                x, t = device_cfg.to_device([x, t])
                y = model.forward(x)
                batch_loss = loss.forward(y, t)

                optimiser.zero_grad()
                batch_loss.backward()
                optimiser.step()
                lrs.step()

                table.update(
                    step=s,
                    epoch=e,
                    batch=i,
                    batch_loss=batch_loss.item(),
                )
                s += 1
                if s >= steps:
                    table.update(level=1, step=s, epoch=e)
                    return

            e += 1

    @classmethod
    def init_sub_objects(
        cls,
        args:       cli.ParsedArgs,
        model:      Model,
        dataset:    Dataset,
    ):
        with cli.verbose:
            optimiser = args.init_object(
                "trainer.BpSpDe.optimiser",
                params=model.parameters(),
            )
            assert isinstance(optimiser, torch.optim.Optimizer)

        scheduler = args.init_object(
            "trainer.BpSpDe.lrs",
            optimizer=optimiser,
            T_max=args.get_value("trainer.BpSpDe.steps"),
        )
        assert isinstance(scheduler, torch.optim.lr_scheduler.LRScheduler)

    @classmethod
    def get_table_columns(cls) -> list[util.Column]:
        return [
            util.TimeColumn("t"),
            util.Column("step"),
            util.Column("epoch"),
            util.Column("batch"),
            util.Column("batch_loss", ".5f", width=10),
            util.CallbackColumn("train_metric", ".5f", width=12),
            util.CallbackColumn("test_metric",  ".5f", width=12),
        ]

    def save_model(self):
        return

    def save_table(self):
        return

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [
            cli.Arg("steps",    type=int, default=int(1e5)),
            cli.Arg("n_train",  type=int, default=int(1e3)),
            *[arg for arg in BpSp.get_cli_options() if arg.name != "epochs"],
        ]

    @classmethod
    def get_tag(cls) -> (str | None):
        return "BSD"
