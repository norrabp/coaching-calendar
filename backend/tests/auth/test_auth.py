from backend.auth.models import User


def test_register(client):
    response = client.post(
        "/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "phone_number": "1234567890",
            "password": "TestUser@2024Secure!",
        },
    )
    assert response.status_code == 201
    assert "user" in response.json
    assert response.json["user"]["username"] == "newuser"
    assert response.json["user"]["email"] == "new@example.com"
    assert response.json["user"]["phone_number"] == "1234567890"


def test_register_duplicate_email(client, test_student):
    response = client.post(
        "/auth/register",
        json={
            "username": "another",
            "email": "unittesting@example.com",
            "phone_number": "1234567890",
            "password": "TestUser@2024Secure!",
        },
    )
    assert response.status_code == 400
    assert "error" in response.json


def test_login_success(client, test_student):
    response = client.post(
        "/auth/login",
        json={"email": "unittesting@example.com", "password": "TestUser@2024Secure!"},
    )
    assert response.status_code == 200
    assert "access_token" in response.json


def test_login_invalid_credentials(client):
    response = client.post(
        "/auth/login", json={"email": "wrong@example.com", "password": "wrongpass"}
    )
    assert response.status_code == 401
    assert "error" in response.json


def test_get_user_profile(client, student_auth_headers):
    response = client.get("/auth/me", headers=student_auth_headers)
    assert response.status_code == 200
    assert "username" in response.json
    assert "email" in response.json


def test_get_user_profile_unauthorized(client):
    response = client.get("/auth/me")
    assert response.status_code == 401
