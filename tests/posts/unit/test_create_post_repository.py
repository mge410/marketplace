from unittest.mock import MagicMock, Mock

import pytest

from src.core.database import PostModel
from src.core.exceptions import UserNotFoundException
from src.posts.exceptions.category_does_not_exists import CategoryDoesNotExistsException
from src.posts.repositories.implementation.create_post_impl import CreatePostImpl


class TestCreatePostRepository:
    @pytest.mark.asyncio
    async def test_create_post_success(
        self, mock_session, create_post_data_schema, author_id, mock_user, mock_category
    ):
        mock_session.execute.side_effect = [
            MagicMock(scalar_one_or_none=Mock(return_value=mock_category)),
            MagicMock(scalar_one_or_none=Mock(return_value=mock_user)),
        ]

        repository = CreatePostImpl(mock_session)
        result = await repository.create(create_post_data_schema, author_id)

        assert mock_session.execute.await_count == 2
        mock_session.add.assert_called_once()
        mock_session.commit.assert_awaited_once()
        mock_session.refresh.assert_awaited_once()
        await self._assert_post_model(mock_user, create_post_data_schema, result)

    @pytest.mark.asyncio
    async def test_create_post_category_not_exists(
        self, mock_session, create_post_data_schema, author_id
    ):
        mock_session.execute.return_value = MagicMock(
            scalar_one_or_none=Mock(return_value=None)
        )

        repository = CreatePostImpl(mock_session)

        with pytest.raises(CategoryDoesNotExistsException):
            await repository.create(create_post_data_schema, author_id)

        assert mock_session.execute.await_count == 1
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_awaited()
        mock_session.refresh.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_create_post_user_not_exists(
        self, mock_session, create_post_data_schema, author_id, mock_category
    ):
        mock_session.execute.side_effect = [
            MagicMock(scalar_one_or_none=Mock(return_value=mock_category)),
            MagicMock(scalar_one_or_none=Mock(return_value=None)),
        ]

        repository = CreatePostImpl(mock_session)

        with pytest.raises(UserNotFoundException):
            await repository.create(create_post_data_schema, author_id)

        assert mock_session.execute.await_count == 2
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_awaited()
        mock_session.refresh.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_check_that_category_exist_success(self, mock_session, mock_category):
        mock_session.execute.return_value = MagicMock(
            scalar_one_or_none=Mock(return_value=mock_category)
        )

        repository = CreatePostImpl(mock_session)

        await repository._check_that_category_exist(1)

    @pytest.mark.asyncio
    async def test_check_that_category_exist_failure(self, mock_session):
        mock_session.execute.return_value = MagicMock(
            scalar_one_or_none=Mock(return_value=None)
        )

        repository = CreatePostImpl(mock_session)

        with pytest.raises(CategoryDoesNotExistsException):
            await repository._check_that_category_exist(1)

    @pytest.mark.asyncio
    async def test_check_that_user_exists_success(
        self, mock_session, mock_user, author_id
    ):
        mock_session.execute.return_value = MagicMock(
            scalar_one_or_none=Mock(return_value=mock_user)
        )

        repository = CreatePostImpl(mock_session)
        result = await repository._check_that_user_exists(author_id)

        assert result == mock_user

    @pytest.mark.asyncio
    async def test_check_that_user_exists_failure(self, mock_session, author_id):
        mock_session.execute.return_value = MagicMock(
            scalar_one_or_none=Mock(return_value=None)
        )

        repository = CreatePostImpl(mock_session)

        with pytest.raises(UserNotFoundException):
            await repository._check_that_user_exists(author_id)

    @staticmethod
    async def _assert_post_model(mock_user, create_post_data_schema, result):
        assert isinstance(result, PostModel)
        assert result.title == create_post_data_schema.title
        assert result.content == create_post_data_schema.content
        assert result.image_url == create_post_data_schema.image_url
        assert result.category_id == create_post_data_schema.category_id
        assert result.author_id == mock_user.id
