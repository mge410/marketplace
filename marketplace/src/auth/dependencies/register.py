from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.repositories.implementation import LoginRepositoryImpl
from src.auth.repositories.implementation import RegisterRepositoryImpl
from src.auth.services.login import LoginService
from src.auth.services.register import RegisterService
from src.core.database import db_helper


def register_service(
    session: AsyncSession = Depends(db_helper.get_session),
) -> RegisterService:
    repository = RegisterRepositoryImpl(session)
    return RegisterService(repository)


def login_service(
    session: AsyncSession = Depends(db_helper.get_session),
) -> LoginService:
    repository = LoginRepositoryImpl(session)
    return LoginService(repository)
