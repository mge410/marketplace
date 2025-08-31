from datetime import datetime, timezone
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
