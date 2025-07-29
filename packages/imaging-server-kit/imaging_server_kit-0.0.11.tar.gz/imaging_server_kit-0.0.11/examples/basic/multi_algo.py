import uvicorn
from imaging_server_kit import MultiAlgorithmServer

from auto_threshold import auto_threshold_algo_server
from threshold import threshold_algo_server

server = MultiAlgorithmServer(
    server_name="multi-algo",
    algorithm_servers=[auto_threshold_algo_server, threshold_algo_server],
)

if __name__ == "__main__":
    uvicorn.run(server.app, host="0.0.0.0", port=8000)
