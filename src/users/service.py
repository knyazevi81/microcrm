from src.models import User, UserRole
from src.dao.base import BaseService


class UserService(BaseService):
    model=User

class UserRoleService(BaseService):
    model=UserRole
