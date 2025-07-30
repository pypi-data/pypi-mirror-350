import torch
import torch.utils.data
from jutility import cli
from juml.datasets.split import DataSplit
from juml.datasets.fromdict import DatasetFromDict

class Synthetic(DatasetFromDict):
    def _init_synthetic(
        self,
        input_shape:    list[int],
        output_shape:   list[int],
        n_train:        int,
        n_test:         int,
        x_std:          float,
        t_std:          float,
    ):
        self._input_shape   = input_shape
        self._output_shape  = output_shape
        self._n_train       = n_train
        self._n_test        = n_test
        self._x_std         = x_std
        self._t_std         = t_std
        self._split_dict    = {
            "train": self._make_split(self._n_train),
            "test":  self._make_split(self._n_test),
        }

    def _make_split(self, n: int) -> DataSplit:
        x = self._sample_input(n)
        t = self._compute_target(x)
        return DataSplit(
            x=x + torch.normal(0, self._x_std, x.shape),
            t=t + torch.normal(0, self._t_std, t.shape),
            n=n,
        )

    def _sample_input(self, n: int) -> torch.Tensor:
        return torch.normal(0, 1, [n, *self._input_shape])

    def _compute_target(self, x: torch.Tensor) -> torch.Tensor:
        raise NotImplementedError()

    def get_loss_weights(self) -> torch.Tensor:
        return 1.0 / self._split_dict["train"].t.flatten(0, -2).std(dim=-2)

    def get_input_shape(self) -> list[int]:
        return self._input_shape

    def get_output_shape(self) -> list[int]:
        return self._output_shape
