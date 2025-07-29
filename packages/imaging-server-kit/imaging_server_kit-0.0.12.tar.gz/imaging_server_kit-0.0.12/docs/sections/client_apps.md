# Client apps

Once an algorithm server is running, you can connect to it and run algorithms from Python, Napari, and QuPath.

## Python client

Use a `Client` instance. For example:

```python
from imaging_server_kit import Client

client = Client("http://localhost:8000")

print(client.algorithms)
# [`rembg`, `stardist`, `cellpose`]

algo_output = client.run_algorithm(
    algorithm="rembg",
    image=(...),
    rembg_model_name="silueta",
)
```

# Napari plugin

Install and use the [Napari Server Kit](https://github.com/Imaging-Server-Kit/napari-serverkit) plugin to connect to algorithm servers and run algorithms in Napari.

# QuPath extension

Install and use the [QuPath Extension Server Kit](https://github.com/Imaging-Server-Kit/qupath-extension-serverkit) to connect to algorithm servers and run algorithms from within QuPath.