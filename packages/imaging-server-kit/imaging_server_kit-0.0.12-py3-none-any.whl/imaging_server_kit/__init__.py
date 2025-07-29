from ._version import version as __version__

try:
    from ._version import version as __version__
except ImportError:
    __version__ = "unknown"

from .client import Client
from .core import (
    algorithm_server,
    AlgorithmServer,
    ParameterUI,
    DropDownUI,
    FloatSpinBoxUI,
    IntSpinBoxUI,
    BoolUI,
    StringUI,
    ImageUI,
    MaskUI,
    PointsUI,
    VectorsUI,
    ShapesUI,
    TracksUI,
    serialize_result_tuple,
    deserialize_result_tuple,
    parse_params,
)
# from .auth import AuthenticatedAlgorithmServer
from .hub import AlgorithmHub, MultiAlgorithmServer
