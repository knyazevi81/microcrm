from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
from datetime import datetime
from typing import Any

from src.users.exceptions import IncorrectTokenFormatException, UserIsNotPresentException
from src.config import settings
from src.users.service import UserService


def get_crm_token(request: Request) -> str:
    token = request.cookies.get("crm_access_token", None)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_crm_token)):
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, settings.ALG)
    except JWTError:
        raise IncorrectTokenFormatException  # noqa: B904

    expire = payload.get("exp")

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="expire is not valid")
    user_id: Any | None = payload.get("sub")

    user = await UserService.find_by_id(int(user_id)) # type: ignore
    if not user_id or not user:
        raise UserIsNotPresentException

    return user


def get_token(request: Request) -> str:
    token = request.cookies.get("booking_access_token", None)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token
