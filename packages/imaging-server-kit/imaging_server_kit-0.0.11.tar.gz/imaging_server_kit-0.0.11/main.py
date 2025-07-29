import uvicorn
from imaging_server_kit.core import Parameters, AlgorithmServer

server = AlgorithmServer(
    algorithm_name="foo", parameters_model=Parameters
)

if __name__ == "__main__":
    uvicorn.run(server.app, host="0.0.0.0", port=8000)
