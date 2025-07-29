"""
Algorithm server definition.
Documentation: https://imaging-server-kit.github.io/imaging-server-kit/
"""
from typing import List
from pathlib import Path
import numpy as np
import uvicorn
from skimage.util import img_as_float
from imaging_server_kit import algorithm_server, ImageUI, FloatSpinBoxUI

# Import your package if needed (also add it to requirements.txt)
# import [...]

@algorithm_server(
    algorithm_name="{{ cookiecutter.project_slug }}",
    title="{{ cookiecutter.project_name }}",
    description="",
    project_url="{{ cookiecutter.project_url }}",
    used_for=["Segmentation"],
    tags=[""],
    parameters={
        "image": ImageUI(
            title="Image",
            description="Input image (2D, 3D)",
            dimensionality=[2, 3],
        ),
        "threshold": FloatSpinBoxUI(
            default=0.5,
            title="Threshold",
            description="Intensity threshold.",
            min=0.0,
            max=1.0,
            step=0.1,
        ),
    },
    sample_images=[str(Path(__file__).parent / "sample_images" / "blobs.tif")],
)
def threshold_algorithm_server(
    image: np.ndarray,
    threshold: float,  # No need to add default values here; instead, add them as `default=` in the Parameters model.
) -> List[tuple]:
    """Runs the algorithm."""
    segmentation = img_as_float(image) > threshold  # Replace this with your code

    segmentation_params = {
        "name": "Threshold result"
    }  # Add information about the result (optional)

    return [
        (segmentation, segmentation_params, "mask")
    ]  # Choose the right output type (`mask` for a segmentation mask)


if __name__ == "__main__":
    uvicorn.run(threshold_algorithm_server.app, host="0.0.0.0", port=8000)
