from datetime import datetime, timezone
from typing import Any, AsyncGenerator
from unittest.mock import AsyncMock, Mock, MagicMock
from uuid import uuid4

import pytest_asyncio
from dotenv import find_dotenv, load_dotenv
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import AsyncSession

env_file = find_dotenv(".env.testing")
load_dotenv(env_file)

from src.core.database import BaseModel, db_helper, UserModel
from src.core.config import settings, Environment
from src.main import main_app
from src.posts.schemes.create_category_schema import CreateCategorySchema
from src.posts.schemes.create_post_schema import CreatePostSchema
from src.auth.repositories.implementation import RegisterRepositoryImpl

@pytest_asyncio.fixture(scope="session", autouse=True)
async def load_env() -> None:
    if settings.app.environment != Environment.TEST:
        raise Exception("Wrong environment")


@pytest_asyncio.fixture(scope="session", autouse=True)
async def migrate_test_db() -> None:
    async with db_helper.engine.begin() as conn:
        await conn.run_sync(BaseModel.metadata.drop_all)
        await conn.run_sync(BaseModel.metadata.create_all)


@pytest_asyncio.fixture(scope="session")
async def db_session() -> AsyncGenerator[AsyncSession, None]:
    async with db_helper.session_factory() as session:
        try:
            yield session
        finally:
            await session.rollback()

@pytest_asyncio.fixture(scope="session")
async def async_client():
    async with AsyncClient(
        transport=ASGITransport(app=main_app), base_url="http://test"
    ) as client:
        yield client


@pytest_asyncio.fixture(scope="session")
async def test_user(db_session: AsyncSession):
    user = UserModel(
        uuid=str(uuid4()),
        email="register@example.com",
        password=RegisterRepositoryImpl._hash_password("correctpassword123"),
        phone="+79123456789",
        name="Иван Петров",
    )

    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    try:
        yield user
    finally:
        await db_session.delete(user)
        await db_session.commit()


@pytest_asyncio.fixture
async def mock_session() -> AsyncMock:
    session = AsyncMock()
    session.add = Mock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    session.delete = AsyncMock()
    return session


@pytest_asyncio.fixture
def mock_post_model():
    post = MagicMock()
    post.id = 1
    post.title = "Test Post"
    post.content = "Test content"
    post.image_url = "http://example.com/image.jpg"
    post.created_at = datetime.now(timezone.utc)
    post.updated_at = datetime.now(timezone.utc)
    post.category_id = 1
    post.author_id = 1
    return post


@pytest_asyncio.fixture
async def create_post_data_schema():
    return CreatePostSchema(
        title="Test Post",
        content="Test content",
        image_url="http://example.com/image.jpg",
        category_id=1,
    )


@pytest_asyncio.fixture
async def author_id():
    return uuid4()


@pytest_asyncio.fixture
async def mock_user():
    user = MagicMock()
    user.id = 1
    user.uuid = uuid4()
    return user


@pytest_asyncio.fixture
def different_user():
    user = MagicMock()
    user.id = 2
    user.uuid = uuid4()
    return user


@pytest_asyncio.fixture
async def mock_category():
    category = MagicMock()
    category.id = 1
    return category


@pytest_asyncio.fixture
async def category_data():
    return CreateCategorySchema(title="test")
