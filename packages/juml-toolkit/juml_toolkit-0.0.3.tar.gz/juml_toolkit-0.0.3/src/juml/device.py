import os
import torch

class DeviceConfig:
    def __init__(self, devices: list[int]):
        self._has_devices = (len(devices) > 0)
        if self._has_devices:
            devices_str = ",".join(str(d) for d in devices)
            os.environ["CUDA_VISIBLE_DEVICES"] = devices_str

    def set_module_device(self, module: torch.nn.Module):
        if self._has_devices:
            module.cuda()

    def to_device(
        self,
        input_tensors: list[torch.Tensor],
    ) -> list[torch.Tensor]:
        if self._has_devices:
            input_tensors = [x.cuda() for x in input_tensors]

        return input_tensors
