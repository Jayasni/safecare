from fastapi.testclient import TestClient


def admin_token(client: TestClient) -> str:
    response = client.post(
        "/api/v1/auth/login",
        json={"email": "admin@test.com", "password": "AdminPass123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def test_admin_can_create_service_and_customer_can_view_it(client: TestClient, admin_user):
    token = admin_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/v1/services",
        json={
            "name": "General Consultation",
            "description": "Basic consultation",
            "duration_minutes": 30,
            "price": "500.00",
            "is_active": True,
        },
        headers=headers,
    )
    assert response.status_code == 201

    public_response = client.get("/api/v1/services")
    assert public_response.status_code == 200
    assert any(service["name"] == "General Consultation" for service in public_response.json())


def test_customer_cannot_create_service(client: TestClient):
    client.post(
        "/api/v1/auth/register",
        json={
            "full_name": "Customer User",
            "email": "customer-service@test.com",
            "password": "password123",
        },
    )
    login_response = client.post(
        "/api/v1/auth/login",
        json={"email": "customer-service@test.com", "password": "password123"},
    )
    token = login_response.json()["access_token"]

    response = client.post(
        "/api/v1/services",
        json={
            "name": "Restricted Service",
            "duration_minutes": 30,
            "price": "100.00",
        },
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 403