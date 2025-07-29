from pathlib import Path

import numpy as np
import orientationpy
import matplotlib
import uvicorn
from imaging_server_kit import (
    DropDownUI,
    FloatSpinBoxUI,
    ImageUI,
    IntSpinBoxUI,
    BoolUI,
    algorithm_server,
)


@algorithm_server(
    algorithm_name="orientationpy",
    parameters={
        "image": ImageUI(),
        "mode": DropDownUI(
            default="fiber",
            title="Mode",
            description="The orientation computation mode.",
            items=["fiber", "membrane"],
        ),
        "scale": FloatSpinBoxUI(
            default=1.0,
            title="Structural scale",
            description="The scale at which orientation is computed.",
            min=0.1,
            max=10.0,
            step=1.0,
        ),
        "with_colors": BoolUI(
            default=False,
            title="Output color-coded orientation",
            description="Whether to output a color-coded representation of orientation or not.",
        ),
        "vector_spacing": IntSpinBoxUI(
            default=3,
            title="Vector spacing",
            description="The spacing at which the orientation vectors are rendered.",
            min=1,
            max=10,
            step=1,
        ),
    },
    sample_images=[
        str(Path(__file__).parent / "sample_images" / "image1_from_OrientationJ.tif"),
    ],
    title="Orientationpy",
    description="An image analysis tool for the measurement of greyscale orientations from 2D or 3D images.",
    project_url="https://gitlab.com/epfl-center-for-imaging/orientationpy",
    used_for=["Filtering"],
    tags=["EPFL"],
)
def orientationpy_server(
    image: np.ndarray,
    mode: str,
    scale: float,
    with_colors: bool,
    vector_spacing: int,
):
    if image.ndim == 2:
        mode = "fiber"  # no membranes in 2D

    gradients = orientationpy.computeGradient(image, mode="splines")
    structureTensor = orientationpy.computeStructureTensor(gradients, sigma=scale)
    orientation_returns = orientationpy.computeOrientation(
        structureTensor,
        mode=mode,
    )
    theta = orientation_returns.get("theta") + 90
    phi = orientation_returns.get("phi")

    boxVectorCoords = orientationpy.anglesToVectors(orientation_returns)

    node_spacings = np.array([vector_spacing] * image.ndim).astype(int)
    slices = [slice(n // 2, None, n) for n in node_spacings]
    grid = np.mgrid[[slice(0, x) for x in image.shape]]
    node_origins = np.stack([g[tuple(slices)] for g in grid])
    slices.insert(0, slice(len(boxVectorCoords)))
    displacements = boxVectorCoords[tuple(slices)].copy()
    displacements *= np.mean(node_spacings)
    displacements = np.reshape(displacements, (image.ndim, -1)).T
    origins = np.reshape(node_origins, (image.ndim, -1)).T
    origins = origins - displacements / 2
    displacement_vectors = np.stack((origins, displacements))
    displacement_vectors = np.rollaxis(displacement_vectors, 1)

    data_tuple = [
        (
            displacement_vectors,
            {
                "name": "Orientation vectors",
                "edge_width": np.max(node_spacings) / 5.0,
                "opacity": 1.0,
                "ndim": image.ndim,
                "edge_color": "blue",
                "vector_style": "line",
            },
            "vectors",
        )
    ]

    if with_colors:
        if image.ndim == 3:
            imDisplayHSV = np.stack(
                (phi / 360, np.sin(np.deg2rad(theta)), image / image.max()), axis=-1
            )
        else:
            imDisplayHSV = np.stack(
                (theta / 180, np.ones_like(image), image / image.max()), axis=-1
            )
        imdisplay_rgb = matplotlib.colors.hsv_to_rgb(imDisplayHSV)

        data_tuple.append(
            (
                imdisplay_rgb,
                {
                    "name": "Color-coded orientation",
                    "rgb": True,
                },
                "image",
            )
        )

    return data_tuple


if __name__ == "__main__":
    uvicorn.run(orientationpy_server.app, host="0.0.0.0", port=8000)
