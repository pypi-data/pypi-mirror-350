# Creating an algorithm server

In this tutorial, we'll re-implement the `serverkit demo` example of an intensity threshold algorithm step-by-step. The working principles and concepts extend to any other algorithm.

## Overview

Implementing an algorithm server with the `imaging-server-kit` involves two main steps:

- Wrapping the image processing logic as a Python function that returns a **list of data tuples**
- Decorating the function with `@algorithm_server`

Let's consider this Python function as an example:

```python
def threshold_algo_server(image: np.ndarray, threshold: float):
    binary_mask = image > threshold
    return binary_mask
```

This function applies an intensity threshold to an image represented as a Numpy array and returns it as a segmentation mask (also a Numpy array).

To turn this function into to an algorithm server, we first need to modify the function to **make it return a list of data tuples**.

## Make the function return a list of data tuples

The function should return a list of tuples. Each tuple has three elements and represents a distinct output of the algorithm.

Our threshold algorithm only has one output: the segmentation mask resulting from thresholding.

```python
def threshold_algo_server(image: np.ndarray, threshold: float):
    binary_mask = image > threshold
    return [(binary_mask, {}, "mask")]  # List of data tuples
```

The data tuples are inspired from Napari's [LayerDataTuple](https://napari.org/0.4.15/guides/magicgui.html?highlight=layerdatatuple) model. They include three elements:

- The *first element* is the **data**, usually in the form of a Numpy array. The shape and interpretation of the axes depends on what the output represents (cf. table below).
- The *second element* is a Python dictionary representing **metadata** associated with the output. It can be empty (`{}`). These metadata are used to affect how the output is displayed in client apps (e.g. Napari).
- The *third element* is the output type: a string identifying what the output represents.

| Output type       | Description                                                                                           |
| ----------------- | ----------------------------------------------------------------------------------------------------- |
| `"image"`         | An image or image-like data (incl. 3D and RGB) as a numpy array.                                         |
| `"mask"`          | A segmentation mask (2D, 3D) as integer numpy array. Integers represent the **object class**.            |
| `"instance_mask"` | A segmentation mask (2D, 3D) as integer nD array. Integers represent **object instances**.            |
| `"points"`        | A collection of point coordinates (array of shape (N, 2) or (N, 3)).                                  |
| `"boxes"`         | A collection of boxes (array of shape (N, 4, 2) representing the box corners). |
| `"vectors"`       | Array of vectors in the Napari [Vectors](https://napari.org/stable/howtos/layers/vectors.html) format.|
| `"tracks"`        | Array of tracks in the Napari [Tracks](https://napari.org/stable/howtos/layers/tracks.html) format.   |
| `"class"`         | A class label (for image classification).                                                             |
| `"text"`          | A string of text (for example, for image captioning).                                                 |

The function can return multiple outputs, following the pattern:

```
# Body of the function
return [
    (data1, {metadata1}, "type1"),  # First output
    (data2, {metadata2}, "type2"),  # Second output
    (...)
]
```

```{admonition} Are there any other constraints on the Python function?
The function parameters can only be **numpy arrays**, **numeric values** (`int`, `float`), **booleans** or **strings**.
```

## Decorate the function with `@algorithm_server`

This has several purposes:

- It converts the python function to a FastAPI server with predefined routes (cf. [API Endpoints](api_endpoints)).
- It enables the server to validate algorithm parameters when receiving requests.
- It tells client apps (Napari, QuPath) how to render the parameters in the user interface.
- Optional info about the algorithm server can be added to populate its `info` page.

Below is our decorated threshold algorithm function:

```python
from imaging_server_kit import algorithm_server, ImageUI, FloatSpinBoxUI

@algorithm_server(
    algorithm_name="threshold",
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
)
def threshold_algo_server(image: np.ndarray, threshold: float):
    binary_mask = image > threshold
    return [(binary_mask, {}, "mask")]

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(threshold_algo_server.app, host="0.0.0.0", port=8000)
```

You can check that running this file as a script will spin up a threshold algorithm server that you can connect to from Napari, QuPath, or Python, just like in the [Getting started](getting_started) guide.

Most importantly, we have specified the `parameters` field of `@algorithm_server`. This enables parameters to be validated by the server before processing. Upon receiving requests with invalid algorithm parameters, the server will reply with a `403` error and an informative message is displayed to the user.

The keys of the `parameters` dictionary should match the parameters of the Python function (in our example: `image` and `threshold`). The values are *parameter UI* elements. There is a UI element for each kind of parameters:

| UI element           | Use case                                                                                                                         |
| -------------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `ImageUI`            | Input image. Validates array dimensionality (by default, accepts `2D` and `3D` arrays).                                          |
| `MaskUI`             | Segmentation mask. Validates array dimensionality (by default, accepts `2D` and `3D` arrays).                                    |
| `DropDownUI`         | A dropdown selector. `items` is used to specify a list of available choices.                                                     |
| `FloatSpinBoxUI`     | Numeric parameter (floating point). Validates `min` and `max` values. `step` can be used to specify a suitable incremental step. |
| `IntSpinBoxUI`       | Numeric parameter (integer). Validates `min` and `max` values. `step` can be used to specify a suitable incremental step.        |
| `BoolUI`             | Boolean parameter, represented as a checkbox.                                                                                    |
| `StringUI`           | String parameter.                                                                                                                |
| `PointsUI`           | Points parameter.                                                                                                                |
| `VectorsUI`          | Vectors parameter.                                                                                                               |
| `ShapesUI`           | Shapes parameter.                                                                                                                |
| `TracksUI`           | Tracks parameter.                                                                                                                |

In our example, the input image array is well-represented by the `ImageUI` element, and the threshold parameter as a `FloatSpinBoxUI`. The parameter defaults and limits (min, max, step) are specified, as well as a title and description of the parameter, which will appear on the algorithm's `info` page.

Moreover, the `@algorithm_server` decorator accepts a variety of optional parameters to enable downloading a sample image, linking to a project page, and providing information on the intended usage of the algorithm server. For details, take a look at the complete [demo example](https://github.com/Imaging-Server-Kit/imaging-server-kit/blob/main/src/imaging_server_kit/demo/threshold.py). The available fields include:

| Key              | Description                                                                                                                      |
| ---------------- | -------------------------------------------------------------------------------------------------------------------------------- |
| `algorithm_name` | A short name for the algorithm server, in URL-friendly format (no spaces or special characters)                                  |
| `title`          | A name or complete title for the algorithm server.                                                                               |
| `description`    | A brief description of the algorithm server.                                                                                     |
| `used_for`       | A list of tags from: `Segmentation`, `Registration`, `Filtering`, `Tracking`, `Restoration`, `Points detection`, `Box detection` |
| `tags`           | Tags used to categorize the algorithm server, for example `Deep learning`, `EPFL`, `Cell biology`, `Digital pathology`.          |
| `project_url`    | A URL string to the project's homepage.                                                                                          |
| `sample_images`  | A list of paths to sample images (`.tif`, `.png`, `.jpg`).                                                                       |

If you provide sample images, the license terms under which the images are distributed should be respected. For example, for images under [CC-BY](https://creativecommons.org/licenses/by/2.0/deed.en) license, proper attribution should be included.

## Starting from a template

It is also possible to create a new algorithm server from a template. Specify an output directory and run the command:

```
serverkit new <output_directory>
```

Running this command will generate the following file structure in the selected output directory:

```
serverkit-project-slug
├── sample_images               # Sample images
│   ├──blobs.tif
└── .gitignore
└── docker-compose.yml          # For deployment with `docker compose up`
└── Dockerfile
└── main.py                     # Implementation of the algorithm server
└── README.md
└── requirements.txt
```

You'll be asked to provide:

- **project_name**: The name of the algorithm or project (e.g. StarDist)
- **project_slug**: A lowercase, URL-friendly name for your project (e.g. stardist)
- **project_url**: A URL to the original project homepage
- **python_version**: The Python version to use (default: `3.9`)

After generating the project structure, you should edit the files to implement the functionality of your algorithm server. You'll have to edit the `main.py` file which implements the algorithm server, as well as the `requirements.txt`. If needed, consider editing the `Dockerfile` and `README.md` to match your use case.
