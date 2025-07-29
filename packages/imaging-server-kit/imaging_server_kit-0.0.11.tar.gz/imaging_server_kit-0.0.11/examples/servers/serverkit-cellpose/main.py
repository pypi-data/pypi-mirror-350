from pathlib import Path
from typing import List

import numpy as np
import uvicorn
from cellpose import models

from imaging_server_kit import (DropDownUI, FloatSpinBoxUI, ImageUI,
                                IntSpinBoxUI, algorithm_server)


@algorithm_server(
    algorithm_name="cellpose",
    parameters={
        "image": ImageUI(
            title="Image",
            description="Input image (2D).",
            dimensionality=[2],
        ),
        "model_name": DropDownUI(
            default="cyto",
            title="Model",
            description="The model used for instance segmentation",
            items=["cyto", "nuclei", "cyto2"],
        ),
        "diameter": IntSpinBoxUI(
            default=20,
            title="Cell diameter (px)",
            description="The approximate size of the objects to detect",
            min=0,
            max=100,
            step=1,
        ),
        "flow_threshold": FloatSpinBoxUI(
            default=0.3,
            title="Flow threshold",
            description="The flow threshold",
            min=0.0,
            max=1.0,
            step=0.05,
        ),
        "cellprob_threshold": FloatSpinBoxUI(
            default=0.5,
            title="Probability threshold",
            description="The detection probability threshold",
            min=0.0,
            max=1.0,
            step=0.01,
        ),
    },
    title="CellPose",
    description="A generalist algorithm for cellular segmentation.",
    used_for=["Segmentation"],
    tags=[
        "Deep learning",
        "Fluorescence microscopy",
        "Digital pathology",
        "Cell biology",
    ],
    project_url="https://github.com/MouseLand/cellpose",
    sample_images=[
        str(Path(__file__).parent / "sample_images" / "nuclei_2d.tif"),
    ],
)
def cellpose_server(
    image: np.ndarray,
    model_name: str,
    diameter: int,
    flow_threshold: float,
    cellprob_threshold: float,
) -> List[tuple]:
    """Runs the algorithm."""
    model = models.CellposeModel(
        gpu=False,  # For now
        model_type=model_name,
    )

    if diameter == 0:
        diameter = None
        print(
            "Diameter is set to None. The size of the cells will be estimated on a per image basis"
        )

    segmentation, flows, styles = model.eval(
        image,
        diameter=diameter,
        flow_threshold=flow_threshold,
        cellprob_threshold=cellprob_threshold,
        channels=[0, 0],  # Grayscale image only (for now)
    )

    segmentation_params = {"name": "Cellpose result"}

    return [
        (segmentation, segmentation_params, "instance_mask"),
    ]


if __name__ == "__main__":
    uvicorn.run(cellpose_server.app, host="0.0.0.0", port=8000)
