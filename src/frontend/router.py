from fastapi import APIRouter, Depends
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from typing import Any

from src.models import User
from src.frontend.dependencies import get_current_user


router = APIRouter()

templates = Jinja2Templates("src/frontend/public")


@router.get("/", include_in_schema=False)
async def base_redirect_page(
    user: User = Depends(get_current_user)
) -> RedirectResponse:
    if user:
        return RedirectResponse('/dashboard')
    return RedirectResponse("/login")


@router.get("/login", include_in_schema=False)
async def login_user_page(
    request: Request,
    user: User = Depends(get_current_user)
) -> Any:
    if user:
        return RedirectResponse("/dashboard")
    return templates.TemplateResponse(
        "login.html",
        {"request": request}
    )

@router.get("/dashboard", include_in_schema=False)
async def dashboard_page(
    request: Request,
    user: User = Depends(get_current_user)
) -> Any:
    if not user:
        return RedirectResponse("/login")
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": user}
    )





