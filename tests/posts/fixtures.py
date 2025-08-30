from unittest.mock import MagicMock, AsyncMock, Mock
from uuid import uuid4

import pytest_asyncio

from src.posts.schemes.create_category_schema import CreateCategorySchema
from src.posts.schemes.create_post_schema import CreatePostSchema


@pytest_asyncio.fixture
async def mock_session() -> AsyncMock:
    session = AsyncMock()
    session.add = Mock()
    session.commit = AsyncMock()
    session.refresh = AsyncMock()
    return session


@pytest_asyncio.fixture
async def post_data():
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
async def mock_category():
    category = MagicMock()
    category.id = 1
    return category


@pytest_asyncio.fixture
async def category_data():
    return CreateCategorySchema(title="test")
