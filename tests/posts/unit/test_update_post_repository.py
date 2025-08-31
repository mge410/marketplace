from unittest.mock import AsyncMock, MagicMock, Mock, patch
from uuid import uuid4

import pytest
from sqlalchemy.exc import NoResultFound

from src.core.database import CategoryModel
from src.core.exceptions import UserNotFoundException
from src.posts.exceptions.category_does_not_exists import CategoryDoesNotExistsException
from src.posts.exceptions.post_not_found_exception import PostNotFoundException
from src.posts.exceptions.user_has_no_access_exception import UserHasNoAccessException
from src.posts.repositories.implementation.update_post_impl import UpdatePostImpl
from src.posts.schemes.update_post_schema import UpdatePostSchema


@pytest.fixture
def mock_category():
    category = MagicMock(spec=CategoryModel)
    category.id = 2
    return category


@pytest.fixture
def update_data():
    return UpdatePostSchema(
        title="New Title",
        content="New Content",
        image_url="http://example.com/new.jpg",
        category_id=2
    )


class TestUpdatePostImpl:
    @pytest.mark.asyncio
    async def test_update_post_success(self, mock_session, mock_post_model, mock_user, mock_category, update_data):
        with patch.object(UpdatePostImpl, '_find_post_by_id', AsyncMock(return_value=mock_post_model)), \
                patch.object(UpdatePostImpl, '_check_author_access', AsyncMock()), \
                patch.object(UpdatePostImpl, '_validate_category_exists', AsyncMock()):
            repository = UpdatePostImpl(mock_session)
            result = await repository.update(mock_post_model.id, update_data, mock_user.uuid)

            assert mock_post_model.title == update_data.title
            assert mock_post_model.content == update_data.content
            assert mock_post_model.image_url == update_data.image_url
            assert mock_post_model.category_id == update_data.category_id

            mock_session.commit.assert_awaited_once()
            mock_session.refresh.assert_awaited_once_with(mock_post_model)

            assert result == mock_post_model

    @pytest.mark.asyncio
    async def test_update_post_not_found(self, mock_session, mock_user, update_data):
        with patch.object(UpdatePostImpl, '_find_post_by_id', AsyncMock(side_effect=PostNotFoundException())):
            repository = UpdatePostImpl(mock_session)

            with pytest.raises(PostNotFoundException):
                await repository.update(999, update_data, mock_user.uuid)

            mock_session.commit.assert_not_awaited()
            mock_session.refresh.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_post_user_not_found(self, mock_session, mock_post_model, update_data):
        with patch.object(UpdatePostImpl, '_find_post_by_id', AsyncMock(return_value=mock_post_model)), \
                patch.object(UpdatePostImpl, '_check_author_access', AsyncMock(side_effect=UserNotFoundException())):
            repository = UpdatePostImpl(mock_session)
            user_id = uuid4()

            with pytest.raises(UserNotFoundException):
                await repository.update(mock_post_model.id, update_data, user_id)

            mock_session.commit.assert_not_awaited()
            mock_session.refresh.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_post_user_no_access(self, mock_session, mock_post_model, mock_user, update_data):
        with patch.object(UpdatePostImpl, '_find_post_by_id', AsyncMock(return_value=mock_post_model)), \
                patch.object(UpdatePostImpl, '_check_author_access', AsyncMock(side_effect=UserHasNoAccessException())):
            repository = UpdatePostImpl(mock_session)

            with pytest.raises(UserHasNoAccessException):
                await repository.update(mock_post_model.id, update_data, mock_user.uuid)

            mock_session.commit.assert_not_awaited()
            mock_session.refresh.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_update_post_category_not_exists(self, mock_session, mock_post_model, mock_user, update_data):
        with patch.object(UpdatePostImpl, '_find_post_by_id', AsyncMock(return_value=mock_post_model)), \
                patch.object(UpdatePostImpl, '_check_author_access', AsyncMock()), \
                patch.object(UpdatePostImpl, '_validate_category_exists',
                             AsyncMock(side_effect=CategoryDoesNotExistsException())):
            repository = UpdatePostImpl(mock_session)

            with pytest.raises(CategoryDoesNotExistsException):
                await repository.update(mock_post_model.id, update_data, mock_user.uuid)

            mock_session.commit.assert_not_awaited()
            mock_session.refresh.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_validate_category_exists_success(self, mock_session, mock_category):
        mock_session.execute.return_value = MagicMock(scalar_one=Mock(return_value=mock_category))

        repository = UpdatePostImpl(mock_session)

        await repository._validate_category_exists(mock_category.id)

        mock_session.execute.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_validate_category_exists_failure(self, mock_session):
        mock_session.execute.return_value = MagicMock(scalar_one=Mock(side_effect=NoResultFound))

        repository = UpdatePostImpl(mock_session)

        with pytest.raises(CategoryDoesNotExistsException):
            await repository._validate_category_exists(999)  # Несуществующий ID категории

        mock_session.execute.assert_awaited_once()