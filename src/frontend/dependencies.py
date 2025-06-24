from fastapi import Request, Depends
from jose import jwt, JWTError
from datetime import datetime
from typing import Any

from src.config import settings
from src.users.service import UserService


def get_crm_token(request: Request) -> str | dict[str, str]:
    token = request.cookies.get("crm_access_token", None)
    if not token:
        return {"detail": 'Unauthorized'}
    return token


async def get_current_user(token: str = Depends(get_crm_token)):
    if isinstance(token, dict) and token.get("detail") == "Unauthorized":
        return None
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALG
        )
    except JWTError:
        return None
    expire = payload.get("exp")

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        return None
    user_id: Any | None = payload.get("sub")
    if not user_id:
        return None
    user = await UserService.find_by_id(int(user_id))
    if not user:
        return None
    return user

