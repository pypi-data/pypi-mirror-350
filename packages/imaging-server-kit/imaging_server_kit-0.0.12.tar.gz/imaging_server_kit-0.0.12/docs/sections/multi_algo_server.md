# Multi-algorithm server

Multiple algorithms can be combined into one server using the `MultiAlgorithmServer` class. Take a look at the example below from the [algorithm server examples](https://github.com/Imaging-Server-Kit/imaging-server-kit/blob/main/examples/basic/multi_algo.py).

```python
from imaging_server_kit import MultiAlgorithmServer

server = MultiAlgorithmServer(
    server_name="multi-algo",
    algorithm_servers=[
      manual_threshold_server,   # Implemented with @algorithm_server
      auto_threshold_server,     # Implemented with @algorithm_server
    ]
)

if __name__ == "__main__":
    uvicorn.run(server.app, host="0.0.0.0", port=8000)
```

When a multi-algorithm server is running, it provides a list of available algorithms under the `/services` route. The code below shows how to interact with a multi-algorithm server from Python:

```python
from imaging_server_kit import Client

client = Client("http://localhost:8000")
print(client.algorithms)  # [`intensity-threshold`, `automatic-threshold`]

results = client.run_algorithm(
  algorithm="intensity-threshold", 
  threshold=0.5,
)
```

In Napari, the available algorithms can be selected from the `algorithms` dropdown. In QuPath, they can be selected from the extensions menu.

```{note}
When using `MultiAlgorithmServer`, all of the algorithms are installed in a single Python environment.
If this is an issue, it's also possible to isolate algorithm servers in Docker containers (see [Using Docker](docker)).
```

