import pytest
from starlette import status


@pytest.mark.asyncio(loop_scope="session")
async def test_login_success(async_client, test_user):
    # prepare
    login_data = {
        "email": "register@example.com",
        "password": "correctpassword123",
    }

    # action
    response = await async_client.post("api/auth/login", json=login_data)

    # assert
    assert response.status_code == status.HTTP_200_OK
    assert "token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "Bearer"
    assert "access_token" in response.cookies


@pytest.mark.asyncio(loop_scope="session")
async def test_login_user_not_found(async_client):
    # prepare
    login_data = {
        "email": "nonexistent@example.com",
        "password": "somepassword123",
    }

    # action
    response = await async_client.post("api/auth/login", json=login_data)

    # assert
    assert response.status_code == status.HTTP_404_NOT_FOUND
    assert "detail" in response.json()


@pytest.mark.asyncio(loop_scope="session")
async def test_login_incorrect_password(async_client, test_user):
    # prepare
    login_data = {
        "email": "register@example.com",
        "password": "wrongpassword123",
    }

    # action
    response = await async_client.post("api/auth/login", json=login_data)

    # assert
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    assert "detail" in response.json()
