from fastapi import APIRouter, Depends
from fastapi.responses import Response
from typing import Any

from src.users.service import UserService
from src.users.schemas import UserRegisterCred, UserRegStatus, UserLogin, UserRefreshPassword
from src.users.exceptions import UserAlreadyExist, IncorrectLoginOrPasswordException
from src.users.auth import get_password_hash, authenticate_user, create_access_token
from src.users.dependencies import get_current_user
from src.models import User


router = APIRouter(prefix="/users", tags=["user api enpoints"])


@router.post("/register")
async def register_users_only_for_admin(
    user_data: UserRegisterCred,
    user: User = Depends(get_current_user)
) -> UserRegStatus:
    existing_user = await UserService.find_one_or_none(username=user_data.username)
    if existing_user:
        raise UserAlreadyExist
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role,
    )
    return UserRegStatus(status=f"User {user_data.username} successfully created!")


@router.post("/login")
async def user_login(
    response: Response,
    user_data: UserLogin
) -> Any:
    user = await authenticate_user(
        user_data.username,
        user_data.password
    )
    if not user:
        raise IncorrectLoginOrPasswordException

    access_token = create_access_token({
        "sub": str(user.id),
        "status": user.role
    })
    response.set_cookie(
        "crm_access_token",
        str(access_token),
        httponly=True
    )
    return access_token


@router.post("/refresh_password")
async def refresh_user_password(
    response: Response,
    user_refresh_data: UserRefreshPassword
) -> Any:
    user = await authenticate_user(
        user_refresh_data.username,
        user_refresh_data.password
    )
    if not user:
        raise IncorrectLoginOrPasswordException
    hashed_password = get_password_hash(user_refresh_data.new_password)
    await UserService.update({
        "username": user_refresh_data.username
    },
    password_hash=hashed_password
    )
    return {"status": "Password successfully changed!"}


@router.post("/logout")
async def logout_user(response: Response):
    response.delete_cookie("crm_access_token")
    return {"status": "User succsessfully logouted"}
