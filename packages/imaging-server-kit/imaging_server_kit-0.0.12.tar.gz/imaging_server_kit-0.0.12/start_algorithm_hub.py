import uvicorn
import imaging_server_kit as serverkit

server = serverkit.AlgorithmHub()

if __name__ == "__main__":
    uvicorn.run(server.app, host="0.0.0.0", port=8000)