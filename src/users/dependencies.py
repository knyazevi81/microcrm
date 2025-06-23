from fastapi import Request, status, Depends
from fastapi.exceptions import HTTPException
from jose import jwt, JWTError
from datetime import datetime
from typing import Any

from src.config import settings
from src.users.service import UserService
from src.models import User


def get_token(request: Request) -> str:
    token = request.cookies.get("crm_access_token", None)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            settings.ALG
        )
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
            detail="token is not JWT"
        ) 
    
    expire = payload.get("exp")

    if (not expire) or (int(expire) < datetime.utcnow().timestamp()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="expire is not valid"
        )
    user_id: Any | None = payload.get("sub")

    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user not fouded",
        )
    user = await UserService.find_by_id(int(user_id))
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="user has not in DB"
        )

    return user

def get_token(request: Request) -> str:
    token = request.cookies.get("booking_access_token", None)
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    return token