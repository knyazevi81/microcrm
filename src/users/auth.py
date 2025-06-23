# pip install passlib python-jose bcrypt

from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt

from src.models import User
from src.users.service import UserService
from src.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    return pwd_context.verify(password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encode_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALG
    )
    return encode_jwt


async def authenticate_user(login: str, password: str) -> User | None:
    user = await UserService.find_one_or_none(login=login)
    if not user:
        return None
    if verify_password(password, user.hashed_password):
        return user
    return None
