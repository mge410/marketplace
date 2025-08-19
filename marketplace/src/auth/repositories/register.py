from abc import ABC, abstractmethod

from src.auth.schemes.register_user import RegisterUserSchema


class RegisterRepository(ABC):
    @abstractmethod
    async def create_user(self, user: RegisterUserSchema) -> RegisterUserSchema:
        pass
