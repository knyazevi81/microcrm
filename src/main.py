from fastapi import FastAPI
from fastapi.requests import Request
from fastapi.responses import RedirectResponse
from starlette.middleware.base import BaseHTTPMiddleware

from contextlib import asynccontextmanager


class NotFoundRedirectMiddleware(BaseHTTPMiddleware):
    """
    Middleware for redirect when trying to enter a non-existent endopoint
    simply redirects to the authentication page
    """
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        if response.status_code == 404:
            return RedirectResponse(url='/login')
        return response


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


def create_app() -> FastAPI:
    _app = FastAPI(
        title="MicroCRM",
        description="Welcome to MIcroCRM API documentation!",
    )

    #_app.mount(
    #    "/static",
    #    StaticFiles(directory="src/frontend/public/static"),
    #    "static"
    #)
    #_app.add_middleware(NotFoundRedirectMiddleware)

    return _app

app = create_app()

@app.get("/ping", include_in_schema=False)
async def ping_pong():
    return {"status": "pong"}
