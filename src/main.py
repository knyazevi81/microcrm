import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi_cache import FastAPICache
from fastapi_cache.backends.redis import RedisBackend

import redis.asyncio as redis
from redis.asyncio.connection import ConnectionPool

from typing import AsyncIterator
from contextlib import asynccontextmanager

from src.frontend.router import router as frontend_router
from src.users.router import router as users_router
from src.users.service import UserRoleService, UserService
from src.users.auth import get_password_hash
from src.config import settings

logger = logging.getLogger("microcrm")
logging.basicConfig(level=logging.INFO)


class NotFoundRedirectMiddleware(BaseHTTPMiddleware):
    """
    Middleware для редиректа в случае ошибки 404
    """

    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 404:
            return RedirectResponse(url="/login")
        return response


async def init_roles_and_root():
    """Инициализация базовых ролей и root-пользователя."""
    # Роли
    for idx, user_role in enumerate(["manager", "admin", "root"], start=1):
        try:
            existing_role = await UserRoleService.find_one_or_none(role=user_role)
            if not existing_role:
                await UserRoleService.add(role=user_role)
                logger.info(f"User role '{user_role}' was created")
        except Exception as e:
            logger.error(f"Failed to create/find role '{user_role}': {e}")

    # Root-пользователь
    try:
        existing_root = await UserService.find_one_or_none(username=settings.ROOT_USERNAME)
        if not existing_root:
            hashed_password = get_password_hash(settings.ROOT_PASSWORD)
            # Получаем id роли root
            root_role = await UserRoleService.find_one_or_none(role="root")
            role_id = root_role.id if root_role else 3
            await UserService.add(
                username=settings.ROOT_USERNAME,
                email=settings.ROOT_EMAIL,
                password_hash=hashed_password,
                full_name="ROOT",
                role=role_id,
            )
            logger.info("Root user was created")
    except Exception as e:
        logger.error(f"Failed to create/find root user: {e}")


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """
    Асинхронный контекст-менеджер жизненного цикла приложения FastAPI.
    Используется для выполнения действий при старте и завершении работы приложения.

    При запуске приложения автоматически добавляет базовые роли пользователей
    ("manager", "admin", "root") в базу данных через UserRoleService.
    """
    await init_roles_and_root()

    try:
        redis_pool = ConnectionPool.from_url(settings.redis_url, decode_responses=True)
        redis_client = redis.Redis(connection_pool=redis_pool)
        FastAPICache.init(RedisBackend(redis_client), prefix="microcrm-cache")  # type: ignore
        logger.info("Redis cache initialized")
    except Exception as e:
        logger.error(f"Failed to initialize Redis cache: {e}")
    yield
    # Здесь можно добавить graceful shutdown для Redis, если потребуется


def create_app() -> FastAPI:
    """
    Создаёт и настраивает экземпляр FastAPI приложения.
    """
    app = FastAPI(
        title="MicroCRM",
        description="Добро пожаловать в документацию MicroCRM API",
        lifespan=lifespan,
    )

    app.include_router(users_router)
    app.include_router(frontend_router)

    app.mount("/static", StaticFiles(directory="src/frontend/public/static"), "static")
    app.add_middleware(NotFoundRedirectMiddleware)

    return app


app = create_app()


@app.get("/ping", include_in_schema=False)
async def ping_pong() -> dict[str, str]:
    """Проверка доступности сервиса."""
    return {"status": "pong"}
