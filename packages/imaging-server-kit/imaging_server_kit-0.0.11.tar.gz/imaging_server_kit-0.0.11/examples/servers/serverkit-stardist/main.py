from pathlib import Path
from typing import List

import numpy as np
import uvicorn
from csbdeep.utils import normalize
from stardist.models import StarDist2D

from imaging_server_kit import (DropDownUI, FloatSpinBoxUI, ImageUI,
                                algorithm_server)


@algorithm_server(
    algorithm_name="stardist",
    parameters={
        "image": ImageUI(
            title="Image",
            description="Input image (2D).",
            dimensionality=[2],
        ),
        "stardist_model_name": DropDownUI(
            default="2D_versatile_fluo",
            title="Model",
            description="The model used for nuclei segmentation",
            items=["2D_versatile_fluo", "2D_versatile_he"],
        ),
        "prob_thresh": FloatSpinBoxUI(
            default=0.5,
            title="Probability threshold",
            description="Predicted object probability threshold",
            min=0.0,
            max=1.0,
            step=0.01,
        ),
        "nms_thresh": FloatSpinBoxUI(
            default=0.4,
            title="Overlap threshold",
            description="Overlapping objects are considered the same when their area/surface overlap exceeds this threshold",
            min=0.0,
            max=1.0,
            step=0.01,
        ),
        "scale": FloatSpinBoxUI(
            default=1.0,
            title="Scale",
            description="Scale the input image internally by this factor and rescale the output accordingly (<1 to downsample, >1 to upsample)",
            min=0.0,
            max=1.0,
            step=0.1,
        ),
    },
    project_url="https://github.com/stardist/stardist",
    title="StarDist (2D)",
    description="Object Detection with Star-convex Shapes.",
    used_for=["Segmentation"],
    tags=[
        "Deep learning",
        "Fluorescence microscopy",
        "H&E",
        "Digital pathology",
        "Cell biology",
        "EPFL",
    ],
    sample_images=[
        str(Path(__file__).parent / "sample_images" / "nuclei_2d.tif"),
    ],
)
def stardist_server(
    image: np.ndarray,
    stardist_model_name: str,
    prob_thresh: float,
    nms_thresh: float,
    scale: float,
) -> List[tuple]:
    """Instance cell nuclei segmentation using StarDist."""
    model = StarDist2D.from_pretrained(stardist_model_name)

    if (image.shape[0] + image.shape[1]) / 2 < 1024:
        segmentation, polys = model.predict_instances(
            normalize(image),
            prob_thresh=prob_thresh,
            nms_thresh=nms_thresh,
            scale=scale,
        )
    else:
        segmentation, polys = model.predict_instances_big(
            normalize(image),
            prob_thresh=prob_thresh,
            nms_thresh=nms_thresh,
            scale=scale,
            block_size=512,
            min_overlap=64,
            axes="YX",
            return_labels=True,
        )

    return [
        (segmentation, {"name": f"{stardist_model_name}_mask"}, "instance_mask"),
    ]


if __name__ == "__main__":
    uvicorn.run(stardist_server.app, host="0.0.0.0", port=8000)
