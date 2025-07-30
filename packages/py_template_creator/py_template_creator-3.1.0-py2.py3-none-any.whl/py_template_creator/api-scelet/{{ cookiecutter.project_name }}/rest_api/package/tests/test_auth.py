import pytest
from package.app.auth.auth_handler import AuthHandler
from package.app.managers import UserManager


@pytest.fixture(scope="function")
async def test_user(session):
    user_data = {
        "email": "test@example.com",
        "password": "SecurePass123!",
        "phone": "+381601234567",
        "display_name": "Test user",
    }

    user_manager = UserManager(session)
    user = await user_manager.create(user_data)
    await session.commit()
    return user


async def test_register(client):
    payload = {
        "email": "newuser@example.com",
        "password": "NewSecurePass123!",
        "phone": "+381607891234",
        "display_name": "Test user",
    }

    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 201
    assert "email" in response.json()
    assert response.json()["email"] == payload["email"]


async def test_register_existing_email(client, test_user):
    payload = {
        "email": test_user.email,
        "password": "SomeNewPass123!",
        "phone": "+381607891234",
        "display_name": "Test user",
    }

    response = client.post("/api/auth/register", json=payload)
    assert response.status_code == 409
    assert response.json()["message"] in [
        "Email already exists",
        "Phone already exists",
    ]


async def test_login_success(client, test_user):
    payload = {"email": test_user.email, "password": "SecurePass123!"}

    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


async def test_login_invalid_credentials(client):
    payload = {
        "email": "test@example.com",
        "password": "WrongPass123!",
    }

    response = client.post("/api/auth/login", json=payload)
    assert response.status_code == 403
    assert response.json()["message"] == "Invalid credentials"


async def test_refresh_token(client, test_user):
    auth_tokens = await AuthHandler.make_auth_tokens(test_user.id)
    payload = {"refresh_token": auth_tokens["refresh_token"]}

    response = client.post("/api/auth/refresh", json=payload)
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "refresh_token" in response.json()


async def test_refresh_invalid_token(client):
    payload = {"refresh_token": "invalid_token_string"}

    response = client.post("/api/auth/refresh", json=payload)
    assert response.status_code == 401
    assert response.json()["message"] == "Invalid refresh token"


async def test_logout(client, test_user):
    auth_tokens = await AuthHandler.make_auth_tokens(test_user.id)
    headers = {"Authorization": f"Bearer {auth_tokens['access_token']}"}
    payload = {"refresh_token": auth_tokens["refresh_token"]}

    response = client.post("/api/auth/logout", json=payload, headers=headers)
    assert response.status_code == 200
    assert response.json()["message"] == "Logged out"
