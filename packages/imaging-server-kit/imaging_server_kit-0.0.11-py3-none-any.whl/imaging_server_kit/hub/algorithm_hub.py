import requests
from fastapi import FastAPI, Request, status, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
import importlib.resources

templates_dir = importlib.resources.files("imaging_server_kit.core").joinpath("templates")
static_dir = importlib.resources.files("imaging_server_kit.core").joinpath("static")

templates = Jinja2Templates(directory=str(templates_dir))


class AlgorithmHub:
    def __init__(self) -> None:
        self.app = FastAPI()
        self.app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
        self.services = {}
        self.register_routes()

    def register_routes(self):
        @self.app.get("/", response_class=HTMLResponse)
        async def home(request: Request):
            services = list(self.services.keys())
            print(f"{services=}")
            return templates.TemplateResponse(
                "index.html",
                {
                    "request": request,
                    "services": services,
                },
            )

        @self.app.get("/services")
        def list_services():
            return {"services": list(self.services.keys())}

        @self.app.post("/register", status_code=status.HTTP_201_CREATED)
        async def register_service(request: Request):
            data = await request.json()
            service_name = data.get("name")
            service_url = data.get("url")
            if service_name in self.services:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Service {service_name} is already registered.",
                )

            self.services[service_name] = service_url
            return {"message": "Service registered"}

        @self.app.post("/deregister", status_code=status.HTTP_201_CREATED)
        async def deregister_service(request: Request):
            data = await request.json()
            service_name = data.get("name")
            if service_name in self.services:
                del self.services[service_name]
                return {"message": "Service deregistered"}
            else:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail=f"Service {service_name} could not be deregistered because it is not in the list of services.",
                )

        @self.app.get("/{algorithm}/info", response_class=HTMLResponse)
        async def get_algorithm_info(request: Request, algorithm: str):
            algo_url = self.services.get(algorithm)
            print(f"{algo_url=}")
            response = requests.get(f"{algo_url}/{algorithm}/info")
            return HTMLResponse(content=response.text, status_code=response.status_code)

        @self.app.get("/{algorithm}/")
        async def get_algorithm(request: Request, algorithm: str):
            algo_url = self.services.get(algorithm)
            response = requests.get(f"{algo_url}/")
            return response.json()

        @self.app.post("/{algorithm}/process", status_code=status.HTTP_201_CREATED)
        async def run_algorithm(algorithm, request: Request):
            algo_url = self.services.get(algorithm)
            data = await request.json()
            response = requests.post(f"{algo_url}/{algorithm}/process", json=data)
            return response.json()

        @self.app.get("/{algorithm}/parameters")
        def get_algorithm_parameters(algorithm):
            algo_url = self.services.get(algorithm)
            response = requests.get(f"{algo_url}/{algorithm}/parameters")
            return response.json()

        @self.app.get("/{algorithm}/sample_images")
        def get_algorithm_sample_images(algorithm):
            algo_url = self.services.get(algorithm)
            response = requests.get(f"{algo_url}/{algorithm}/sample_images")
            return response.json()
