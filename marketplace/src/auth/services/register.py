from src.auth.jwt import utils as jwt_utils
from src.auth.repositories.register import RegisterRepository
from src.auth.schemes.login_user import TokenInfo
from src.auth.schemes.register_user import RegisterUserSchema


class RegisterService:
    def __init__(self, repository: RegisterRepository):
        self.repository = repository

    async def register_user(self, user: RegisterUserSchema) -> TokenInfo:
        user = await self.repository.create_user(user)
        token_info = await jwt_utils.create_jwt_token(user)
        return token_info
