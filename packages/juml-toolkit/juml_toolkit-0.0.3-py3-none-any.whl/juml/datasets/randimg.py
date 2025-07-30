import torch
from jutility import cli
from juml.datasets.split import DataSplit
from juml.datasets.synthetic import Synthetic
from juml.loss.base import Loss
from juml.loss.mse import Mse
from juml.loss.crossentropy import CrossEntropy

class RandomClassification(Synthetic):
    def __init__(
        self,
        input_shape:    list[int],
        output_shape:   list[int],
        train:          int,
        test:           int,
    ):
        self._init_synthetic(
            input_shape=input_shape,
            output_shape=output_shape,
            n_train=train,
            n_test=test,
            x_std=0,
            t_std=0,
        )

    def _make_split(self, n: int) -> DataSplit:
        return DataSplit(
            x=torch.rand([n, *self._input_shape]),
            t=torch.randint(
                low=0,
                high=self._output_shape[-1],
                size=[n, *self._output_shape[:-1]],
            ),
            n=n,
        )

    @classmethod
    def get_default_loss(cls) -> type[Loss] | None:
        return CrossEntropy

    @classmethod
    def get_cli_arg(cls):
        return cli.ObjectArg(
            cls,
            cli.Arg("input_shape",  type=int, nargs="+", default=[3, 32, 32]),
            cli.Arg("output_shape", type=int, nargs="+", default=[10]),
            cli.Arg("train",        type=int, default=200),
            cli.Arg("test",         type=int, default=200),
        )

class RandomRegression(RandomClassification):
    def _make_split(self, n: int) -> DataSplit:
        return DataSplit(
            x=torch.rand([n, *self._input_shape]),
            t=torch.rand([n, *self._output_shape]),
            n=n,
        )

    @classmethod
    def get_default_loss(cls) -> type[Loss] | None:
        return Mse
