from pydantic import BaseModel
from enum import Enum

class UserEnumRole(int, Enum):
    manager = 1
    admin = 2
    root = 3

class UserRegisterCred(BaseModel):
    username: str
    email: str
    password: str
    full_name: str
    role: UserEnumRole

class UserRegStatus(BaseModel):
    status: str
