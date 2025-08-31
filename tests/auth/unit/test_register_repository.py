import pytest
from unittest.mock import AsyncMock, MagicMock

from src.auth.repositories.implementation import RegisterRepositoryImpl
from src.auth.schemes.register_user import RegisterUserSchema
from src.auth.exceptions.multiple_validation_exception import (
    MultipleValidationException,
)
from src.core.database import UserModel


class TestRegisterRepositoryImpl:
    @pytest.fixture
    def register_repository(self, mock_session):
        return RegisterRepositoryImpl(mock_session)

    @pytest.fixture
    def user_data(self):
        return RegisterUserSchema(
            email="test@example.com",
            password="password123",
            phone="+79998887766",
            name="John",
        )

    @pytest.fixture
    def existing_user(self):
        return UserModel(
            id=1,
            email="existing@example.com",
            phone="+0987654321",
            password="hashed_password",
        )

    @pytest.mark.asyncio
    async def test_create_user_success(
        self, register_repository, mock_session, user_data
    ):
        # prepare
        mock_session.execute.return_value = MagicMock(
            scalar_one_or_none=MagicMock(return_value=None)
        )
        mock_session.commit = AsyncMock()

        # action
        result = await register_repository.create_user(user_data)

        # assert
        assert isinstance(result, UserModel)
        assert result.email == user_data.email
        assert result.phone == user_data.phone
        assert result.name == user_data.name
        assert result.password != user_data.password
        mock_session.add.assert_called_once()
        mock_session.commit.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_unique_user_both_exist(
        self, register_repository, mock_session, user_data, existing_user
    ):
        # prepare
        mock_result_email = MagicMock()
        mock_result_email.scalar_one_or_none.return_value = existing_user

        mock_result_phone = MagicMock()
        mock_result_phone.scalar_one_or_none.return_value = existing_user

        mock_session.execute.side_effect = [mock_result_email, mock_result_phone]

        # action & assert
        with pytest.raises(MultipleValidationException) as exc_info:
            await register_repository._check_unique_user(user_data)

        assert len(exc_info.value.errors) == 2
        assert any(error.field == "email" for error in exc_info.value.errors)
        assert any(error.field == "phone" for error in exc_info.value.errors)

    @pytest.mark.asyncio
    async def test_check_unique_user_email_exists(
        self, register_repository, mock_session, user_data, existing_user
    ):
        # prepare
        mock_result_email = MagicMock()
        mock_result_email.scalar_one_or_none.return_value = existing_user

        mock_result_phone = MagicMock()
        mock_result_phone.scalar_one_or_none.return_value = None

        mock_session.execute.side_effect = [mock_result_email, mock_result_phone]

        # action & assert
        with pytest.raises(MultipleValidationException) as exc_info:
            await register_repository._check_unique_user(user_data)

        assert len(exc_info.value.errors) == 1
        assert exc_info.value.errors[0].field == "email"

    @pytest.mark.asyncio
    async def test_check_unique_user_phone_exists(
        self, register_repository, mock_session, user_data, existing_user
    ):
        # prepare
        mock_result_email = MagicMock()
        mock_result_email.scalar_one_or_none.return_value = None

        mock_result_phone = MagicMock()
        mock_result_phone.scalar_one_or_none.return_value = existing_user

        mock_session.execute.side_effect = [mock_result_email, mock_result_phone]

        # action & assert
        with pytest.raises(MultipleValidationException) as exc_info:
            await register_repository._check_unique_user(user_data)

        assert len(exc_info.value.errors) == 1
        assert exc_info.value.errors[0].field == "phone"

    @pytest.mark.asyncio
    async def test_check_unique_user_no_errors(
        self, register_repository, mock_session, user_data
    ):
        # prepare
        mock_result_email = MagicMock()
        mock_result_email.scalar_one_or_none.return_value = None

        mock_result_phone = MagicMock()
        mock_result_phone.scalar_one_or_none.return_value = None

        mock_session.execute.side_effect = [mock_result_email, mock_result_phone]

        # action
        await register_repository._check_unique_user(user_data)

        # assert
        assert mock_session.execute.call_count == 2

    @pytest.mark.asyncio
    async def test_check_unique_user_by_email_exists(
        self, register_repository, mock_session, user_data, existing_user
    ):
        # prepare
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_user
        mock_session.execute.return_value = mock_result

        # action
        result = await register_repository._check_unique_user_by_email(user_data)

        # assert
        assert result is not None
        assert result.field == "email"
        assert "already exists" in result.message
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_unique_user_by_email_not_exists(
        self, register_repository, mock_session, user_data
    ):
        # prepare
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        # action
        result = await register_repository._check_unique_user_by_email(user_data)

        # assert
        assert result is None
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_unique_user_by_phone_exists(
        self, register_repository, mock_session, user_data, existing_user
    ):
        # prepare
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = existing_user
        mock_session.execute.return_value = mock_result

        # action
        result = await register_repository._check_unique_user_by_phone(user_data)

        # assert
        assert result is not None
        assert result.field == "phone"
        assert "already exists" in result.message
        mock_session.execute.assert_called_once()

    @pytest.mark.asyncio
    async def test_check_unique_user_by_phone_not_exists(
        self, register_repository, mock_session, user_data
    ):
        # prepare
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        # action
        result = await register_repository._check_unique_user_by_phone(user_data)

        # assert
        assert result is None
        mock_session.execute.assert_called_once()

    def test_hash_password(self, register_repository):
        # prepare
        password = "testpassword"

        # action
        hashed_password = register_repository._hash_password(password)

        # assert
        assert hashed_password != password
        assert isinstance(hashed_password, str)
