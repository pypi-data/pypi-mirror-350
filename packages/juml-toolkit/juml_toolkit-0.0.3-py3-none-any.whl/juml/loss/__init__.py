from juml.loss.base import Loss
from juml.loss.crossentropy import CrossEntropy
from juml.loss.mse import Mse
from juml.loss.asmse import AlignedSetMse
from juml.loss.chamfer import ChamferMse

def get_all() -> list[type[Loss]]:
    return [
        CrossEntropy,
        Mse,
        AlignedSetMse,
        ChamferMse,
    ]
