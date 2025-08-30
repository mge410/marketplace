from typing import Optional
from unittest.mock import MagicMock, Mock

import pytest

from src.core.database import CategoryModel
from src.posts.exceptions.category_already_exists_exception import (
    CategoryAlreadyExistsException,
)
from src.posts.repositories.implementation.create_category_impl import (
    CreateCategoryImpl,
)
from src.posts.schemes.create_category_schema import CreateCategorySchema


class TestCreateCategoryRepository:
    @pytest.mark.asyncio
    async def test_success_create_category(self, mock_session, category_data):
        await self._mock_query(None, mock_session)

        repository = CreateCategoryImpl(mock_session)
        result = await repository.create_category(category_data)

        mock_session.execute.assert_awaited_once()
        mock_session.add.assert_called_once()
        mock_session.commit.assert_awaited_once()

        assert isinstance(result, CategoryModel)
        assert result.title == category_data.title

    @pytest.mark.asyncio
    async def test_exception_already_exists_category(self, mock_session, category_data):
        await self._mock_query(category_data, mock_session)

        repository = CreateCategoryImpl(mock_session)

        with pytest.raises(CategoryAlreadyExistsException):
            await repository.create_category(category_data)

        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_awaited()

    @staticmethod
    async def _mock_query(category_data: Optional[CreateCategorySchema], mock_session):
        mock_session.add = Mock()
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = category_data
        mock_session.execute.return_value = mock_result
