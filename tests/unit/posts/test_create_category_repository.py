from unittest.mock import AsyncMock, MagicMock, Mock

import pytest

from src.core.database import CategoryModel
from src.posts.exceptions.category_already_exists_exception import CategoryAlreadyExistsException
from src.posts.repositories.implementation.create_category_impl import CreateCategoryImpl
from src.posts.schemes.create_category_schema import CreateCategorySchema


class TestCreateCategoryRepository:
    @pytest.mark.asyncio
    async def test_create_category(self):
        mock_session = AsyncMock()
        mock_session.add = Mock()
        mock_session.commit = AsyncMock()

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        repository = CreateCategoryImpl(mock_session)
        category_data = CreateCategorySchema(title="test")
        result = await repository.create_category(category_data)

        mock_session.execute.assert_awaited_once()

        mock_session.add.assert_called_once()
        mock_session.commit.assert_awaited_once()

        assert isinstance(result, CategoryModel)
        assert result.title == "test"

    @pytest.mark.asyncio
    async def test_create_category_already_exists(self):
        mock_session = AsyncMock()
        mock_session.add = Mock()
        mock_session.commit = AsyncMock()

        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = CategoryModel(title="test")
        mock_session.execute.return_value = mock_result

        repository = CreateCategoryImpl(mock_session)
        category_data = CreateCategorySchema(title="test")

        with pytest.raises(CategoryAlreadyExistsException):
            await repository.create_category(category_data)

        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_awaited()
