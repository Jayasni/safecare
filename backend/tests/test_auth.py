from fastapi.testclient import TestClient


def test_register_login_and_me(client: TestClient):
    response = client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "customer@test.com",
            "password": "password123",
        },
    )
    assert response.status_code == 201
    assert response.json()["role"] == "customer"

    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "customer@test.com", "password": "password123"},
    )
    assert login_response.status_code == 200
    token = login_response.json()["access_token"]

    me_response = client.get(
        "/api/v1/auth/me", headers={"Authorization": f"Bearer {token}"}
    )
    assert me_response.status_code == 200
    assert me_response.json()["email"] == "customer@test.com"


def test_duplicate_registration_rejected(client: TestClient):
    payload = {
        "full_name": "Test User",
        "email": "duplicate@test.com",
        "password": "password123",
    }
    assert client.post("/api/v1/auth/register", json=payload).status_code == 201
    assert client.post("/api/v1/auth/register", json=payload).status_code == 409


def test_invalid_login_rejected(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Test User",
            "email": "login@test.com",
            "password": "password123",
        },
    )
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "login@test.com", "password": "wrong-password"},
    )
    assert response.status_code == 401


def test_me_requires_authentication(client: TestClient):
    response = client.get("/api/v1/auth/me")
    assert response.status_code == 401