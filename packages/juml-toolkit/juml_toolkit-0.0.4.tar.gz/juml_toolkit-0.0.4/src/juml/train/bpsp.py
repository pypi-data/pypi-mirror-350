import torch
from jutility import cli, util
from juml.device import DeviceConfig
from juml.train.base import Trainer
from juml.models.base import Model
from juml.datasets.base import Dataset
from juml.loss.base import Loss

class BpSp(Trainer):
    def train(
        self,
        args:       cli.ParsedArgs,
        model:      Model,
        dataset:    Dataset,
        loss:       Loss,
        device_cfg: DeviceConfig,
        table:      util.Table,
        batch_size: int,
        epochs:     int,
        optimiser:  torch.optim.Optimizer,
        lrs:        torch.optim.lr_scheduler.LRScheduler,
    ):
        train_loader = dataset.get_data_loader("train", batch_size)
        test_loader  = dataset.get_data_loader("test" , batch_size)

        table.get_column("train_metric").set_callback(
            lambda: loss.metric(model, train_loader, device_cfg),
            level=1,
        )
        table.get_column("test_metric").set_callback(
            lambda: loss.metric(model, test_loader, device_cfg),
            level=1,
        )

        for e in range(epochs):
            table.update(level=1, epoch=e)
            for i, (x, t) in enumerate(train_loader):
                x, t = device_cfg.to_device([x, t])
                y = model.forward(x)
                batch_loss = loss.forward(y, t)

                optimiser.zero_grad()
                batch_loss.backward()
                optimiser.step()

                table.update(epoch=e, batch=i, batch_loss=batch_loss.item())

            table.print_last()
            lrs.step()

        table.update(level=2, epoch=epochs)

    @classmethod
    def init_sub_objects(
        cls,
        args:       cli.ParsedArgs,
        model:      Model,
        dataset:    Dataset,
    ):
        with cli.verbose:
            optimiser = args.init_object(
                "trainer.BpSp.optimiser",
                params=model.parameters(),
            )
            assert isinstance(optimiser, torch.optim.Optimizer)

        scheduler = args.init_object(
            "trainer.BpSp.lrs",
            optimizer=optimiser,
            T_max=args.get_value("trainer.BpSp.epochs"),
        )
        assert isinstance(scheduler, torch.optim.lr_scheduler.LRScheduler)

    @classmethod
    def get_table_columns(cls) -> list[util.Column]:
        return [
            util.TimeColumn("t"),
            util.Column("epoch"),
            util.Column("batch"),
            util.Column("batch_loss", ".5f", width=10),
            util.CallbackColumn("train_metric", ".5f", width=12),
            util.CallbackColumn("test_metric",  ".5f", width=12),
        ]

    @classmethod
    def get_cli_options(cls) -> list[cli.Arg]:
        return [
            cli.Arg("batch_size",   type=int, default=100),
            cli.Arg("epochs",       type=int, default=1),
            cli.ObjectChoice(
                "optimiser",
                cli.ObjectArg(
                    torch.optim.Adam,
                    cli.Arg("lr", type=float, default=0.001),
                ),
                cli.ObjectArg(
                    torch.optim.AdamW,
                    cli.Arg("lr",           type=float, default=0.001),
                    cli.Arg("weight_decay", type=float, default=0.01),
                    tag="AW",
                ),
                cli.ObjectArg(
                    torch.optim.SGD,
                    cli.Arg("lr",           type=float, default=0.001),
                    cli.Arg("momentum",     type=float, default=0.0),
                    cli.Arg("weight_decay", type=float, default=0.0),
                ),
                default="Adam",
            ),
            cli.ObjectChoice(
                "lrs",
                cli.ObjectArg(
                    torch.optim.lr_scheduler.CosineAnnealingLR,
                    cli.Arg("eta_min", type=float, default=1e-5),
                ),
                default="CosineAnnealingLR",
            ),
        ]
