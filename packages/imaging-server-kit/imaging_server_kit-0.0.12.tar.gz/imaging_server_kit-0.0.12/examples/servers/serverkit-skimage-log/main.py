from pathlib import Path
from typing import List

import numpy as np
import skimage.feature
import uvicorn
from skimage.util import img_as_float

from imaging_server_kit import (
    BoolUI,
    FloatSpinBoxUI,
    ImageUI,
    IntSpinBoxUI,
    algorithm_server,
)


@algorithm_server(
    algorithm_name="skimage-LoG",
    parameters={
        "image": ImageUI(),
        "min_sigma": FloatSpinBoxUI(
            default=5.0,
            title="Min sigma",
            description="Minimum standard deviation of the Gaussian kernel, in pixels.",
            min=0.1,
            max=100.0,
            step=0.1,
        ),
        "max_sigma": FloatSpinBoxUI(
            default=10.0,
            title="Max sigma",
            description="Maximum standard deviation of the Gaussian kernel, in pixels.",
            min=0.1,
            max=100.0,
            step=0.1,
        ),
        "num_sigma": IntSpinBoxUI(
            default=10,
            title="Num sigma",
            description="Number of intermediate sigma values to compute between the min_sigma and max_sigma.",
            min=1,
            max=100,
            step=1,
        ),
        "threshold": FloatSpinBoxUI(
            default=0.1,
            title="Threshold",
            description="Lower bound for scale space maxima.",
            min=0.01,
            max=1.0,
            step=0.01,
        ),
        "invert_image": BoolUI(
            default=False,
            title="Dark blobs",
            description="Whether to invert the image before computing the LoG filter.",
        ),
        "time_dim": BoolUI(
            default=True,
            title="Frame by frame",
            description="Only applicable to 3D images. If set, the first dimension is considered time and the LoG is computed independently for every frame.",
        ),
    },
    sample_images=[
        str(Path(__file__).parent / "sample_images" / "blobs.tif"),
        str(Path(__file__).parent / "sample_images" / "tracks.tif"),
    ],
    title="LoG detector (Scikit-image)",
    description="Implementation of a Laplacian of Gaussian (LoG) detector in Scikit-image.",
    project_url="https://scikit-image.org/docs/stable/api/skimage.feature.html#skimage.feature.blob_log",
    used_for=["Points detection"],
    tags=["Scikit-image", "3D"],
)
def skimage_log_server(
    image: np.ndarray,
    max_sigma: float,
    num_sigma: int,
    threshold: float,
    invert_image: bool,
    time_dim: bool,
    min_sigma: float,
) -> List[tuple]:
    """Runs a LoG detector for blob detection."""
    if invert_image:
        image = -image

    image = img_as_float(image)

    if (image.ndim == 3) & time_dim:
        # Handle a time-series
        points = np.empty((0, 3))
        sigmas = []
        for frame_id, frame in enumerate(image):
            frame_results = skimage.feature.blob_log(
                frame,
                min_sigma=min_sigma,
                max_sigma=max_sigma,
                num_sigma=num_sigma,
                threshold=threshold,
            )
            frame_points = frame_results[:, :2]  # Shape (N, 2)
            frame_sigmas = list(frame_results[:, 2])  # Shape (N,)
            sigmas.extend(frame_sigmas)
            frame_points = np.hstack(
                (np.array([frame_id] * len(frame_points))[..., None], frame_points)
            )  # Shape (N, 3)
            points = np.vstack((points, frame_points))
        sigmas = np.array(sigmas)
    else:
        results = skimage.feature.blob_log(
            image,
            min_sigma=min_sigma,
            max_sigma=max_sigma,
            num_sigma=num_sigma,
            threshold=threshold,
        )
        points = results[:, :2]
        sigmas = results[:, 2]

    points_params = {
        "name": "Detections",
        "opacity": 0.7,
        "face_color": "sigma",
        "features": {
            "sigma": sigmas
        },  # sigmas = numpy array representing the point size
    }

    if len(points):
        return [
            (points, points_params, "points"),
        ]
    else:
        return [
            ("No points were detected.", {}, "text")
        ]


if __name__ == "__main__":
    uvicorn.run(skimage_log_server.app, host="0.0.0.0", port=8000)
