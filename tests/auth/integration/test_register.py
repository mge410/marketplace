from unittest.mock import AsyncMock, patch

import pytest
from fastapi import status

from src.auth.exceptions.multiple_validation_exception import (
    MultipleValidationException,
    ValidationError,
)


@pytest.mark.asyncio(loop_scope="session")
async def test_register_success(async_client):
    # prepare
    with patch(
        "src.auth.use_cases.register.broker.publish", new_callable=AsyncMock
    ) as mock_publish:
        user_data = {
            "email": "test@example.com",
            "password": "strongpassword123",
            "phone": "+79998882211",
            "name": "Иван Петров",
        }

        # action
        response = await async_client.post("api/auth/register", json=user_data)
        print(response.json())
        # assert
        assert response.status_code == status.HTTP_200_OK
        assert response.json() == {"success": True}

        mock_publish.assert_called_once()
        assert "access_token" in response.cookies


@pytest.mark.asyncio(loop_scope="session")
async def test_register_duplicate_email(async_client):
    # prepare
    with patch(
        "src.auth.repositories.register.RegisterRepository.create_user"
    ) as mock_create:
        mock_create.side_effect = MultipleValidationException(
            [
                ValidationError(
                    field="email",
                    message="User with this email already exists",
                    value="test@example.com",
                )
            ]
        )

        user_data = {
            "email": "test@example.com",
            "password": "strongpassword123",
            "phone": "+79998882211",
            "name": "Иван Петров",
        }

        # action
        response = await async_client.post("api/auth/register", json=user_data)

        # assert
        assert response.status_code == status.HTTP_400_BAD_REQUEST
        print(response.json()["detail"][0]["field"])
        assert "email" in response.json()["detail"][0]["field"]


@pytest.mark.asyncio(loop_scope="session")
async def test_register_invalid_phone(async_client):
    # prepare
    user_data = {
        "email": "test@example.com",
        "password": "strongpassword123",
        "phone": "invalid_phone",
        "name": "Иван Петров",
    }

    # action
    response = await async_client.post("api/auth/register", json=user_data)

    # assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    assert "phone" in response.text


@pytest.mark.asyncio(loop_scope="session")
async def test_register_missing_required_fields(async_client):
    # prepare
    user_data = {
        "email": "test@example.com",
    }

    # action
    response = await async_client.post("api/auth/register", json=user_data)

    # assert
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
