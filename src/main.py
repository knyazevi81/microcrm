from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from contextlib import asynccontextmanager

from src.users.router import router as users_router
from src.users.service import UserRoleService, UserService
from src.users.auth import get_password_hash
from src.config import settings


class NotFoundRedirectMiddleware(BaseHTTPMiddleware):
    """
    Middleware для редиректа в случае ошибки 404
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 404:
            return RedirectResponse(url="/login")
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Асинхронный контекст-менеджер жизненного цикла приложения FastAPI.
    Используется для выполнения действий при старте и завершении работы приложения.

    При запуске приложения автоматически добавляет базовые роли пользователей
    ("manager", "admin", "root") в базу данных через UserRoleService.
    """
    # Create users roles
    for user_role in ["manager", "admin", "root"]:  # Base roles
        await UserRoleService.add(role=user_role)
        print(f"User role {user_role} was created")
    # Create root user
    existing_root = await UserService.find_one_or_none(username=settings.ROOT_USERNAME)
    if not existing_root:
        hashed_password = get_password_hash(settings.ROOT_PASSWORD)
        await UserService.add(
            username=settings.ROOT_USERNAME,
            email=settings.ROOT_EMAIL,
            password_hash=hashed_password,
            full_name="ROOT",
            role=3,
        )
    yield


def create_app() -> FastAPI:
    _app = FastAPI(
        title="MicroCRM",
        description="Добро пожаловать в документацию MicroCRM API",
        lifespan=lifespan,
    )

    _app.include_router(users_router)

    # _app.mount(
    #    "/static",
    #    StaticFiles(directory="src/frontend/public/static"),
    #    "static"
    # )
    # _app.add_middleware(NotFoundRedirectMiddleware)

    return _app


app = create_app()


@app.get("/ping", include_in_schema=False)
async def ping_pong():
    return {"status": "pong"}
