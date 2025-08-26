from src.auth.exceptions import IncorrectPasswordException
from src.auth.exceptions import UserNotFoundException
from src.auth.jwt import utils as jwt_utils
from src.auth.repositories.login import LoginRepository
from src.auth.schemes.login_user import LoginUserSchema, TokenInfo


class LoginUseCase:
    def __init__(self, repository: LoginRepository):
        self.repository = repository

    async def login(self, user_login_data: LoginUserSchema) -> TokenInfo:
        user = await self.repository.get_user_by_email(str(user_login_data.email))
        if not user:
            raise UserNotFoundException

        if not await self.repository.check_user_password(user, user_login_data):
            raise IncorrectPasswordException

        token_info = await jwt_utils.create_jwt_token(user)
        return token_info
