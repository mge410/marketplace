from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repositories.implementation import LoginRepositoryImpl
from src.auth.repositories.implementation import RegisterRepositoryImpl
from src.auth.use_cases.login import LoginUseCase
from src.auth.use_cases.register import RegisterUseCase
from src.core.database import db_helper


def register_use_case(
    session: AsyncSession = Depends(db_helper.get_session),
) -> RegisterUseCase:
    repository = RegisterRepositoryImpl(session)
    return RegisterUseCase(repository)


def login_use_case(
    session: AsyncSession = Depends(db_helper.get_session),
) -> LoginUseCase:
    repository = LoginRepositoryImpl(session)
    return LoginUseCase(repository)
