import bcrypt
import pytest
from unittest.mock import MagicMock

from src.auth.repositories.implementation import LoginRepositoryImpl
from src.auth.schemes.login_user import LoginUserSchema
from src.core.database import UserModel


class TestLoginRepositoryImpl:
    @pytest.fixture
    def login_repository(self, mock_session):
        return LoginRepositoryImpl(mock_session)

    @pytest.fixture
    def sample_user(self):
        salt = bcrypt.gensalt()
        password = bcrypt.hashpw("password123".encode(), salt).decode()
        user = UserModel(id=1, email="test@example.com", password=password)
        return user

    @pytest.fixture
    def login_data_correct(self):
        return LoginUserSchema(email="test@example.com", password="password123")

    @pytest.fixture
    def login_data_incorrect(self):
        return LoginUserSchema(email="test@example.com", password="wrongpassword")

    @pytest.mark.asyncio
    async def test_get_user_by_email_found(
        self, login_repository, mock_session, sample_user
    ):
        # prepare
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = sample_user
        mock_session.execute.return_value = mock_result

        # action
        result = await login_repository.get_user_by_email("test@example.com")

        # assert
        mock_session.execute.assert_called_once()
        assert result == sample_user

    @pytest.mark.asyncio
    async def test_get_user_by_email_not_found(self, login_repository, mock_session):
        # prepare
        mock_result = MagicMock()
        mock_result.scalar_one_or_none.return_value = None
        mock_session.execute.return_value = mock_result

        # action
        result = await login_repository.get_user_by_email("nonexistent@example.com")

        # assert
        mock_session.execute.assert_called_once()
        assert result is None

    @pytest.mark.asyncio
    async def test_check_user_password_correct(
        self, login_repository, sample_user, login_data_correct
    ):
        # action
        result = await login_repository.check_user_password(
            sample_user, login_data_correct
        )

        # assert
        assert result is True

    @pytest.mark.asyncio
    async def test_check_user_password_incorrect(
        self, login_repository, sample_user, login_data_incorrect
    ):
        # action
        result = await login_repository.check_user_password(
            sample_user, login_data_incorrect
        )

        # assert
        assert result is False

    @pytest.mark.asyncio
    async def test_validate_password_correct(self, login_repository):
        # prepare
        password = "testpassword"
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # action
        result = login_repository._validate_password(password, hashed_password)

        # assert
        assert result is True

    @pytest.mark.asyncio
    async def test_validate_password_incorrect(self, login_repository):
        # prepare
        password = "testpassword"
        wrong_password = "wrongpassword"
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

        # action
        result = login_repository._validate_password(wrong_password, hashed_password)

        # assert
        assert result is False
