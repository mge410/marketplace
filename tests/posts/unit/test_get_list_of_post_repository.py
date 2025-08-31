import unittest
from typing import Sequence
from unittest.mock import MagicMock

import pytest

from src.core.database import PostModel, CategoryModel
from src.posts.repositories.implementation.get_list_of_posts_impl import (
    GetListOfPostsImpl,
)
from src.posts.schemes.post_query_schema import PostQuerySchema


@pytest.fixture
def mock_posts():
    post1 = MagicMock(spec=PostModel)
    post1.id = 1
    post1.title = "Post 1"
    post1.content = "Content 1"
    post1.category = MagicMock(spec=CategoryModel)
    post1.category.id = 1
    post1.category.title = "Category 1"

    post2 = MagicMock(spec=PostModel)
    post2.id = 2
    post2.title = "Post 2"
    post2.content = "Content 2"
    post2.category = MagicMock(spec=CategoryModel)
    post2.category.id = 2
    post2.category.title = "Category 2"

    return [post1, post2]


@pytest.fixture
def post_query_params():
    return PostQuerySchema(
        page_number=1,
        page_size=10,
    )


class TestGetListOfPostsImpl:
    @pytest.mark.asyncio
    async def test_get_list_of_posts_success(
        self, mock_session, mock_posts, post_query_params
    ):
        # prepare
        mock_result = MagicMock()
        mock_result.scalars.return_value.unique.return_value.all.return_value = (
            mock_posts
        )
        mock_session.execute.return_value = mock_result
        with (
            unittest.mock.patch.object(GetListOfPostsImpl, "filter") as mock_filter,
            unittest.mock.patch.object(GetListOfPostsImpl, "paginate") as mock_paginate,
        ):
            mock_query = MagicMock()
            mock_filter.return_value = mock_query
            mock_paginate.return_value = mock_query
            repository = GetListOfPostsImpl(mock_session)

            # action
            result = await repository.get_list_of_posts(post_query_params)

            # assert
            mock_filter.assert_called_once()
            mock_paginate.assert_called_once()
            mock_session.execute.assert_awaited_once_with(mock_query)
            assert isinstance(result, Sequence)
            assert len(result) == len(mock_posts)
            for i, post in enumerate(result):
                assert post.id == mock_posts[i].id
                assert post.title == mock_posts[i].title

    @pytest.mark.asyncio
    async def test_get_list_of_posts_empty(self, mock_session, post_query_params):
        # prepare
        mock_result = MagicMock()
        mock_result.scalars.return_value.unique.return_value.all.return_value = []
        mock_session.execute.return_value = mock_result
        with (
            unittest.mock.patch.object(GetListOfPostsImpl, "filter") as mock_filter,
            unittest.mock.patch.object(GetListOfPostsImpl, "paginate") as mock_paginate,
        ):
            mock_query = MagicMock()
            mock_filter.return_value = mock_query
            mock_paginate.return_value = mock_query
            repository = GetListOfPostsImpl(mock_session)

            # action
            result = await repository.get_list_of_posts(post_query_params)

            # assert
            mock_filter.assert_called_once()
            mock_paginate.assert_called_once()
            mock_session.execute.assert_awaited_once_with(mock_query)
            assert isinstance(result, Sequence)
            assert len(result) == 0

    @pytest.mark.asyncio
    async def test_get_list_of_posts_with_filters(self, mock_session, mock_posts):
        # prepare
        mock_result = MagicMock()
        mock_result.scalars.return_value.unique.return_value.all.return_value = (
            mock_posts
        )
        mock_session.execute.return_value = mock_result
        filtered_query_params = PostQuerySchema(
            page_number=1, page_size=5, category_id=1, search="test"
        )

        with (
            unittest.mock.patch.object(GetListOfPostsImpl, "filter") as mock_filter,
            unittest.mock.patch.object(GetListOfPostsImpl, "paginate") as mock_paginate,
        ):
            mock_query = MagicMock()
            mock_filter.return_value = mock_query
            mock_paginate.return_value = mock_query
            repository = GetListOfPostsImpl(mock_session)

            # action
            result = await repository.get_list_of_posts(filtered_query_params)

            # assert
            mock_filter.assert_called_once()
            mock_paginate.assert_called_once()
            mock_session.execute.assert_awaited_once_with(mock_query)
            assert isinstance(result, Sequence)
            assert len(result) == len(mock_posts)

    @pytest.mark.asyncio
    async def test_initial_query_includes_selectinload(
        self, mock_session, post_query_params
    ):
        # prepare
        repository = GetListOfPostsImpl(mock_session)
        with (
            unittest.mock.patch.object(GetListOfPostsImpl, "filter") as mock_filter,
            unittest.mock.patch.object(GetListOfPostsImpl, "paginate") as mock_paginate,
        ):
            mock_query = MagicMock()
            mock_filter.return_value = mock_query
            mock_paginate.return_value = mock_query

            mock_result = MagicMock()
            mock_result.scalars.return_value.unique.return_value.all.return_value = []
            mock_session.execute.return_value = mock_result

            # action
            await repository.get_list_of_posts(post_query_params)
            # assert
            mock_session.execute.assert_awaited_once_with(mock_query)
