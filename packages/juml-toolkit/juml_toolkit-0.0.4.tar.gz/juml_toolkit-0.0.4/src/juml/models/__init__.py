from juml.models import embed, pool

from juml.models.base import Model
from juml.models.sequential import Sequential
from juml.models.embed import Embedder
from juml.models.pool import Pooler
from juml.models.linear import Linear
from juml.models.linearmodel import LinearModel
from juml.models.mlp import Mlp
from juml.models.rzmlp import RzMlp, ReZeroMlpLayer
from juml.models.cnn import Cnn
from juml.models.rzcnn import RzCnn

def get_all() -> list[type[Model]]:
    return [
        LinearModel,
        Mlp,
        RzMlp,
        Cnn,
        RzCnn,
    ]
