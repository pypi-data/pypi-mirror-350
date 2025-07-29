from pathlib import Path
from typing import List

import numpy as np
import pandas as pd
import trackpy as tp
import uvicorn

from imaging_server_kit import IntSpinBoxUI, PointsUI, algorithm_server


@algorithm_server(
    algorithm_name="trackpy",
    parameters={
        "points": PointsUI(
            title="Points",
            description="The points to track.",
            dimensionality=[2, 3],
        ),
        "search_range": IntSpinBoxUI(
            default=30,
            title="Search range",
            description="Search range in pixels.",
            max=100,
        ),
        "memory": IntSpinBoxUI(
            default=3,
            title="Memory",
            description="Maximum number of skipped frames for a single track.",
            max=10,
        ),
    },
    project_url="https://soft-matter.github.io/trackpy/",
    title="Trackpy",
    description="Fast, Flexible Particle-Tracking Toolkit.",
    used_for=["Tracking"],
    sample_images=[
        str(Path(__file__).parent / "sample_images" / "tracks.tif"),
    ],
)
def trackpy_server(
    points: np.ndarray,
    search_range: int,
    memory: int,
) -> List[tuple]:
    """Runs the algorithm."""
    df = pd.DataFrame(
        {
            "frame": points[:, 0],
            "y": points[:, 1],
            "x": points[:, 2],
        }
    )

    linkage_df = tp.link(df, search_range=search_range, memory=memory)

    tracks = linkage_df[["particle", "frame", "y", "x"]].values.astype(float)

    return [(tracks, {"name": "Tracks"}, "tracks")]


if __name__ == "__main__":
    uvicorn.run(trackpy_server.app, host="0.0.0.0", port=8000)
