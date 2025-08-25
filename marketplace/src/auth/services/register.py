from src.auth.jwt import utils as jwt_utils
from src.auth.repositories.register import RegisterRepository
from src.auth.schemes.login_user import TokenInfo
from src.auth.schemes.register_user import RegisterUserSchema
from src.core.config import settings
from src.core.fs_broker import broker


class RegisterService:
    def __init__(self, repository: RegisterRepository):
        self.repository = repository

    async def register_user(
        self, register_user_schema: RegisterUserSchema
    ) -> TokenInfo:
        user_model = await self.repository.create_user(register_user_schema)
        token_info = await jwt_utils.create_jwt_token(user_model)
        await broker.publish(
            routing_key=settings.faststream.user_registered_event,
            message=user_model.email,
        )

        return token_info
