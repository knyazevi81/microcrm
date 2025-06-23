from fastapi import APIRouter

from src.users.service import UserService
from src.users.schemas import UserRegisterCred, UserRegStatus
from src.users.exceptions import UserAlreadyExist
from src.users.auth import get_password_hash


router = APIRouter(
    prefix="/users",
    tags=["user api enpoints"]
)


@router.post("/register")
async def register_users_only_for_admin(
    user_data: UserRegisterCred
) -> UserRegStatus:
    existing_user = await UserService.find_one_or_none(
        username=user_data.username
    )
    if existing_user:
        raise UserAlreadyExist
    hashed_password = get_password_hash(user_data.password)
    await UserService.add(
        username=user_data.username,
        email=user_data.email,
        password_hash=hashed_password,
        full_name=user_data.full_name,
        role=user_data.role
    )
    return UserRegStatus(status=f"User {user_data.username} successfully created!")

