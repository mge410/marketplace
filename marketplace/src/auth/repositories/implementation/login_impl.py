import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repositories.login import LoginRepository
from src.auth.schemes.login_user import LoginUserSchema
from src.core.database import UserModel


class LoginRepositoryImpl(LoginRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_user_by_email(self, email: str) -> UserModel | None:
        stmt = select(UserModel).where(UserModel.email == email)
        result = await self.session.execute(stmt)
        return result.scalar_one_or_none()

    async def check_user_password(
        self,
        user: UserModel,
        user_login_data: LoginUserSchema,
    ) -> bool:
        return self._validate_password(user_login_data.password, user.password)

    @staticmethod
    def _validate_password(password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(
            password=password.encode(), hashed_password=hashed_password.encode()
        )
