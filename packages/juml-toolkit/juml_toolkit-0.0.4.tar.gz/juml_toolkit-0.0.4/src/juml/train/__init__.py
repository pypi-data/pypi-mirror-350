from juml.train.base import Trainer
from juml.train.bpsp import BpSp
from juml.train.bpspde import BpSpDe

def get_all() -> list[type[Trainer]]:
    return [
        BpSp,
        BpSpDe,
    ]
