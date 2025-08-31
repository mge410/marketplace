from unittest.mock import MagicMock, Mock
from uuid import uuid4

import pytest
from sqlalchemy.exc import NoResultFound

from src.core.database.models import DeletedPostModel
from src.core.exceptions import UserNotFoundException
from src.posts.exceptions.post_not_found_exception import PostNotFoundException
from src.posts.exceptions.user_has_no_access_exception import UserHasNoAccessException
from src.posts.repositories.implementation.delete_post_impl import DeletePostImpl


class TestDeletePostImpl:
    @pytest.mark.asyncio
    async def test_delete_post_success(self, mock_session, mock_post_model, mock_user):
        mock_session.execute.side_effect = [
            MagicMock(scalar_one=Mock(return_value=mock_post_model)),
            MagicMock(scalar_one=Mock(return_value=mock_user))
        ]

        repository = DeletePostImpl(mock_session)
        user_id = mock_user.uuid

        await repository.delete(mock_post_model.id, user_id)
        assert mock_session.execute.await_count == 2

        mock_session.delete.assert_awaited_once_with(mock_post_model)
        mock_session.add.assert_called_once()
        added_args = mock_session.add.call_args[0]
        assert len(added_args) == 1
        deleted_post = added_args[0]

        assert isinstance(deleted_post, DeletedPostModel)
        assert deleted_post.title == mock_post_model.title
        assert deleted_post.content == mock_post_model.content
        assert deleted_post.image_url == mock_post_model.image_url
        assert deleted_post.created_at == mock_post_model.created_at
        assert deleted_post.updated_at == mock_post_model.updated_at
        assert deleted_post.category_id == mock_post_model.category_id
        assert deleted_post.author_id == mock_post_model.author_id
        assert deleted_post.deleted_at is not None

        mock_session.commit.assert_awaited_once()

    @pytest.mark.asyncio
    async def test_delete_post_not_found(self, mock_session, mock_user):
        mock_session.execute.side_effect = [
            MagicMock(scalar_one=Mock(side_effect=NoResultFound)),
            MagicMock(scalar_one=Mock(return_value=mock_user))
        ]

        repository = DeletePostImpl(mock_session)
        user_id = mock_user.uuid

        with pytest.raises(PostNotFoundException):
            await repository.delete(999, user_id)

        mock_session.delete.assert_not_called()
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_post_user_not_found(self, mock_session, mock_post_model):
        mock_session.execute.side_effect = [
            MagicMock(scalar_one=Mock(return_value=mock_post_model)),
            MagicMock(scalar_one=Mock(side_effect=NoResultFound))
        ]

        repository = DeletePostImpl(mock_session)
        user_id = uuid4()

        with pytest.raises(UserNotFoundException):
            await repository.delete(mock_post_model.id, user_id)

        mock_session.delete.assert_not_called()
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_delete_post_user_no_access(self, mock_session, mock_post_model, different_user):
        mock_session.execute.side_effect = [
            MagicMock(scalar_one=Mock(return_value=mock_post_model)),
            MagicMock(scalar_one=Mock(return_value=different_user))
        ]

        repository = DeletePostImpl(mock_session)
        user_id = different_user.uuid

        with pytest.raises(UserHasNoAccessException):
            await repository.delete(mock_post_model.id, user_id)

        mock_session.delete.assert_not_called()
        mock_session.add.assert_not_called()
        mock_session.commit.assert_not_awaited()

    @pytest.mark.asyncio
    async def test_find_post_by_id_success(self, mock_session, mock_post_model):
        mock_session.execute.return_value = MagicMock(
            scalar_one=Mock(return_value=mock_post_model)
        )

        repository = DeletePostImpl(mock_session)
        result = await repository._find_post_by_id(mock_post_model.id)

        assert result == mock_post_model

    @pytest.mark.asyncio
    async def test_find_post_by_id_not_found(self, mock_session):
        mock_session.execute.return_value = MagicMock(
            scalar_one=Mock(side_effect=NoResultFound)
        )

        repository = DeletePostImpl(mock_session)

        with pytest.raises(PostNotFoundException):
            await repository._find_post_by_id(999)  # Несуществующий ID поста

    @pytest.mark.asyncio
    async def test_check_author_access_success(self, mock_session, mock_post_model, mock_user):
        mock_session.execute.return_value = MagicMock(
            scalar_one=Mock(return_value=mock_user)
        )

        repository = DeletePostImpl(mock_session)

        await repository._check_author_access(mock_post_model, mock_user.uuid)

    @pytest.mark.asyncio
    async def test_check_author_access_user_not_found(self, mock_session, mock_post_model):
        mock_session.execute.return_value = MagicMock(
            scalar_one=Mock(side_effect=NoResultFound)
        )

        repository = DeletePostImpl(mock_session)

        with pytest.raises(UserNotFoundException):
            await repository._check_author_access(mock_post_model, uuid4())

    @pytest.mark.asyncio
    async def test_check_author_access_no_access(self, mock_session, mock_post_model, different_user):
        mock_session.execute.return_value = MagicMock(
            scalar_one=Mock(return_value=different_user)
        )

        repository = DeletePostImpl(mock_session)

        with pytest.raises(UserHasNoAccessException):
            await repository._check_author_access(mock_post_model, different_user.uuid)
