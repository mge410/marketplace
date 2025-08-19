from abc import ABC, abstractmethod

from src.auth.schemes.login_user import LoginUserSchema
from src.core.database import UserModel


class LoginRepository(ABC):
    @abstractmethod
    async def get_user_by_email(self, email: str) -> UserModel | None:
        pass

    @abstractmethod
    async def check_user_password(self, user: UserModel, user_login_data: LoginUserSchema) -> bool:
        pass
