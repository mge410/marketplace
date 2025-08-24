from typing import Optional

import bcrypt
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.exceptions.MultipleValidationException import MultipleValidationException, ValidationError
from src.auth.repositories.register import RegisterRepository
from src.auth.schemes.register_user import RegisterUserSchema
from src.core.database import UserModel


class RegisterRepositoryImpl(RegisterRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_user(
            self,
            user_data: RegisterUserSchema,
    ) -> UserModel:
        await self._check_unique_user(user_data)
        user = UserModel(
            **user_data.model_dump(exclude={'password'}),
            password=self._hash_password(password=user_data.password)
        )
        self.session.add(user)
        await self.session.commit()
        return user

    async def _check_unique_user(self, user_data):
        errors = []
        email_error = await self._check_unique_user_by_email(user_data)
        if email_error:
            errors.append(email_error)
        phone_error = await self._check_unique_user_by_phone(user_data)
        if phone_error:
            errors.append(phone_error)

        if errors:
            raise MultipleValidationException(errors)

    async def _check_unique_user_by_phone(self, user_data) -> Optional[ValidationError]:
        existing_phone = await self.session.execute(
            select(UserModel).where(UserModel.phone == user_data.phone)
        )
        if existing_phone.scalar_one_or_none():
            return ValidationError(
                field="phone",
                message="User with this phone already exists",
                value=user_data.phone
            )
        return None

    async def _check_unique_user_by_email(self, user_data) -> Optional[ValidationError]:
        existing_user = await self.session.execute(
            select(UserModel).where(UserModel.email == user_data.email)
        )
        if existing_user.scalar_one_or_none():
            return ValidationError(
                field="email",
                message="User with this email already exists",
                value=user_data.email
            )
        return None

    @staticmethod
    def _hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        return bcrypt.hashpw(password.encode(), salt).decode()
