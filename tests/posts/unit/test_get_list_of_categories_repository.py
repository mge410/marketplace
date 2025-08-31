from typing import Sequence
from unittest.mock import MagicMock

import pytest

from src.core.database import CategoryModel
from src.posts.repositories.implementation.get_list_of_categories_impl import GetListOfCategoriesImpl


@pytest.fixture
def mock_categories():
    category1 = MagicMock(spec=CategoryModel)
    category1.id = 1
    category1.title = "Category 1"

    category2 = MagicMock(spec=CategoryModel)
    category2.id = 2
    category2.title = "Category 2"

    return [category1, category2]

class TestGetListOfCategoriesImpl:
    @pytest.mark.asyncio
    async def test_get_list_of_categories_success(self, mock_session, mock_categories):
        mock_result = MagicMock()
        mock_result.scalars.return_value.all.return_value = mock_categories
        mock_session.execute.return_value = mock_result

        repository = GetListOfCategoriesImpl(mock_session)
        result = await repository.get_list_of_categories()

        mock_session.execute.assert_awaited_once()

        assert isinstance(result, Sequence)

        assert len(result) == len(mock_categories)

        for i, category in enumerate(result):
            assert category.id == mock_categories[i].id
            assert category.title == mock_categories[i].title
