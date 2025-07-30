import torch.utils.data
import torchvision
from juml.datasets import DATA_REL_DIR
from juml.datasets.fromdict import DatasetFromDict
from juml.loss.base import Loss
from juml.loss.crossentropy import CrossEntropy

class Mnist(DatasetFromDict):
    def _get_split_dict(self) -> dict[str, torch.utils.data.Dataset]:
        return {
            "train": torchvision.datasets.MNIST(
                root=DATA_REL_DIR,
                train=True,
                transform=torchvision.transforms.ToTensor(),
                download=True,
            ),
            "test": torchvision.datasets.MNIST(
                root=DATA_REL_DIR,
                train=False,
                transform=torchvision.transforms.ToTensor(),
                download=True,
            ),
        }

    def get_input_shape(self) -> list[int]:
        return [1, 28, 28]

    def get_output_shape(self) -> list[int]:
        return [10]

    @classmethod
    def get_default_loss(cls) -> type[Loss] | None:
        return CrossEntropy
