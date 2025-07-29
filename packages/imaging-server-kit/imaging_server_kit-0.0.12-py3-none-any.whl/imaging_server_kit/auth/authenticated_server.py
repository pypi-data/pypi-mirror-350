
"""
Algorithm server protected by user authentication. ⚠️ It isn't fully working yet!
"""
import importlib.resources
from fastapi import FastAPI, Request, status, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from contextlib import asynccontextmanager

from imaging_server_kit import AlgorithmServer

from .utils import (
    create_db_and_tables,
    fastapi_users,
    auth_backend,
    UserRead,
    UserUpdate,
    UserCreate,
    User,
    current_active_user,
)

static_dir = importlib.resources.files("imaging_server_kit.auth").joinpath("static")
templates_dir = importlib.resources.files("imaging_server_kit.auth").joinpath("templates")
templates = Jinja2Templates(directory=str(templates_dir))

class AuthenticatedAlgorithmServer(AlgorithmServer):
    def __init__(
        self,
    ):
        super.__init__(self)

        # Users
        self.app.include_router(
            fastapi_users.get_auth_router(auth_backend),
            prefix="/auth/jwt",
            tags=["auth"],
        )
        self.app.include_router(
            fastapi_users.get_register_router(UserRead, UserCreate),
            prefix="/auth",
            tags=["auth"],
        )
        self.app.include_router(
            fastapi_users.get_reset_password_router(),
            prefix="/auth",
            tags=["auth"],
        )
        self.app.include_router(
            fastapi_users.get_verify_router(UserRead),
            prefix="/auth",
            tags=["auth"],
        )
        self.app.include_router(
            fastapi_users.get_users_router(UserRead, UserUpdate),
            prefix="/users",
            tags=["users"],
        )

        self.register_routes()

    @asynccontextmanager
    async def lifespan(self, app: FastAPI):
        await self.register_with_algohub()  # TODO: this is weirdly overwritten. Is there a better way of handling this lifespan?
        create_db_and_tables()
        yield
        await self.deregister_from_algohub()

    def register_extra_routes(self):
        @self.app.get(f"/register", response_class=HTMLResponse)
        def register(request: Request):
            return templates.TemplateResponse("register.html", {"request": request})

        @self.app.get(f"/login", response_class=HTMLResponse)
        def login(request: Request):
            return templates.TemplateResponse("login.html", {"request": request})

        @self.app.post(
            f"/{self.algorithm_name}/process", status_code=status.HTTP_201_CREATED
        )
        async def run_algo(
            algo_params: self.parameters_model,
            user: User = Depends(current_active_user),
        ):
            return await self._run_algo_logic(algo_params)