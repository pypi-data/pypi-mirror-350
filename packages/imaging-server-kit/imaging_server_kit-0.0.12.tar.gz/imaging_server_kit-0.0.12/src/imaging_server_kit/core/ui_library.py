from typing import List

try:
    from typing import Literal
except ImportError:
    from typing_extensions import Literal


class ParameterUI:
    def __init__(self, title: str = "", description: str = ""):
        self.title = title
        self.description = description
        self.type = str
        self.widget_type = None


class DropDownUI(ParameterUI):
    def __init__(
        self,
        title="Choice",
        description="Dropdown selection",
        items: List = [],
        default: str = None,
    ):
        super().__init__(title, description)
        self.type = Literal.__getitem__(tuple(items))
        self.default = default
        self.widget_type = "dropdown"


class FloatSpinBoxUI(ParameterUI):
    def __init__(
        self,
        title="Float",
        description="Numeric parameter (floating point)",
        min: float = 0.0,
        max: float = 1000.0,
        step: float = 0.1,
        default: float = None,
    ):
        super().__init__(title, description)
        self.min = min
        self.max = max
        self.step = step
        self.type = float
        self.default = default
        self.widget_type = "float"


class IntSpinBoxUI(ParameterUI):
    def __init__(
        self,
        title="Int",
        description="Numeric parameter (integer)",
        min: int = 0,
        max: int = 1000,
        step: int = 1,
        default: int = None,
    ):
        super().__init__(title, description)
        self.min = min
        self.max = max
        self.step = step
        self.type = int
        self.default = default
        self.widget_type = "int"


class BoolUI(ParameterUI):
    def __init__(
        self,
        title="Bool",
        description="Boolean parameter",
        default: bool = None,
    ):
        super().__init__(title, description)
        self.type = bool
        self.default = default
        self.widget_type = "bool"


class StringUI(ParameterUI):
    def __init__(
        self,
        title="String",
        description="String parameter",
        default: str = None,
    ):
        super().__init__(title, description)
        self.type = str
        self.default = default
        self.widget_type = "str"


class ImageUI(ParameterUI):
    def __init__(
        self,
        title="Image",
        description="Input image (2D, 3D)",
        dimensionality: List[int] = [2, 3],
    ):
        super().__init__(title, description)
        self.widget_type = "image"
        self.dimensionality = dimensionality


class MaskUI(ParameterUI):
    def __init__(
        self,
        title="Mask",
        description="Segmentation mask (2D, 3D)",
        dimensionality: List[int] = [2, 3],
    ):
        super().__init__(title, description)
        self.widget_type = "mask"
        self.dimensionality = dimensionality


class PointsUI(ParameterUI):
    def __init__(
        self,
        title="Points",
        description="Input points (2D, 3D)",
        dimensionality: List[int] = [2, 3],
    ):
        super().__init__(title, description)
        self.widget_type = "points"
        self.dimensionality = dimensionality


class VectorsUI(ParameterUI):
    def __init__(
        self,
        title="Vectors",
        description="Input vectors (2D, 3D)",
        dimensionality: List[int] = [2, 3],
    ):
        super().__init__(title, description)
        self.widget_type = "vectors"
        self.dimensionality = dimensionality


class ShapesUI(ParameterUI):
    def __init__(
        self,
        title="Shapes",
        description="Input shapes",
    ):
        super().__init__(title, description)
        self.widget_type = "shapes"


class TracksUI(ParameterUI):
    def __init__(
        self,
        title="Tracks",
        description="Input tracks",
    ):
        super().__init__(title, description)
        self.widget_type = "tracks"
