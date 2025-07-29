from pathlib import Path
import numpy as np
import uvicorn
from imaging_server_kit import algorithm_server, ImageUI, FloatSpinBoxUI
from skimage.util import img_as_float


@algorithm_server(
    algorithm_name="intensity-threshold",
    title="Binary Threshold",
    description="Implementation of a binary threshold algorithm.",
    used_for=["Segmentation"],
    tags=["Demo"],
    parameters={
        "image": ImageUI(),
        "threshold": FloatSpinBoxUI(
            default=0.5,
            min=0.0,
            max=1.0,
            step=0.1,
            title="Threshold",
            description="Intensity threshold.",
        ),
    },
    sample_images=[str(Path(__file__).parent / "sample_images" / "blobs.tif")],
)
def threshold_algo_server(
    image: np.ndarray,
    threshold: float,
):
    """Implements a simple intensity threshold algorithm."""
    mask = img_as_float(image) > threshold
    return [(mask, {"name": "Threshold result"}, "mask")]


if __name__ == "__main__":
    uvicorn.run(threshold_algo_server.app, host="0.0.0.0", port=8000)
