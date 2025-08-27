from abc import ABC, abstractmethod

from src.auth.schemes.register_user import RegisterUserSchema
from src.core.database import UserModel


class RegisterRepository(ABC):
    @abstractmethod
    async def create_user(self, user: RegisterUserSchema) -> UserModel:
        pass
