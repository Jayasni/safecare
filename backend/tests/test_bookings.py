from fastapi.testclient import TestClient


def get_token(client: TestClient, email: str, password: str) -> str:
    response = client.post("/api/v1/auth/login", json={"email": email, "password": password})
    assert response.status_code == 200
    return response.json()["access_token"]


def auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}"}


def setup_service_slot(client: TestClient, admin_token: str, capacity: int = 1):
    service_response = client.post(
        "/api/v1/services",
        json={
            "name": "Test Service",
            "description": "Test",
            "duration_minutes": 30,
            "price": "100.00",
        },
        headers=auth_headers(admin_token),
    )
    assert service_response.status_code == 201
    service_id = service_response.json()["id"]

    provider_response = client.post(
        "/api/v1/providers",
        json={"full_name": "Test Provider", "specialization": "General", "is_active": True},
        headers=auth_headers(admin_token),
    )
    assert provider_response.status_code == 201
    provider_id = provider_response.json()["id"]

    from datetime import datetime, timedelta, timezone

    start = (datetime.now(timezone.utc) + timedelta(hours=2)).replace(microsecond=0)
    end = start + timedelta(minutes=30)
    slot_response = client.post(
        "/api/v1/availability",
        json={
            "service_id": service_id,
            "provider_id": provider_id,
            "start_time": start.isoformat(),
            "end_time": end.isoformat(),
            "capacity": capacity,
            "is_active": True,
        },
        headers=auth_headers(admin_token),
    )
    assert slot_response.status_code == 201
    return slot_response.json()["id"]


def test_customer_can_book_and_duplicate_is_rejected(client: TestClient, admin_user):
    admin_token = get_token(client, "admin@test.com", "AdminPass123")
    slot_id = setup_service_slot(client, admin_token, capacity=2)

    client.post(
        "/api/v1/auth/register",
        json={"full_name": "Customer One", "email": "customer1@test.com", "password": "password123"},
    )
    customer_token = get_token(client, "customer1@test.com", "password123")

    first = client.post(
        "/api/v1/bookings",
        json={"slot_id": slot_id, "reason": "Visit"},
        headers=auth_headers(customer_token),
    )
    assert first.status_code == 201
    booking_id = first.json()["id"]

    duplicate = client.post(
        "/api/v1/bookings",
        json={"slot_id": slot_id, "reason": "Second attempt"},
        headers=auth_headers(customer_token),
    )
    assert duplicate.status_code == 409

    cancel = client.patch(f"/api/v1/bookings/{booking_id}/cancel", headers=auth_headers(customer_token))
    assert cancel.status_code == 200
    assert cancel.json()["status"] == "cancelled"


def test_slot_capacity_cannot_be_exceeded(client: TestClient, admin_user):
    admin_token = get_token(client, "admin@test.com", "AdminPass123")
    slot_id = setup_service_slot(client, admin_token, capacity=1)

    client.post("/api/v1/auth/register", json={"full_name": "Customer A", "email": "custa@test.com", "password": "password123"})
    client.post("/api/v1/auth/register", json={"full_name": "Customer B", "email": "custb@test.com", "password": "password123"})
    token_a = get_token(client, "custa@test.com", "password123")
    token_b = get_token(client, "custb@test.com", "password123")

    first = client.post("/api/v1/bookings", json={"slot_id": slot_id, "reason": "A"}, headers=auth_headers(token_a))
    assert first.status_code == 201

    second = client.post("/api/v1/bookings", json={"slot_id": slot_id, "reason": "B"}, headers=auth_headers(token_b))
    assert second.status_code == 409


def test_admin_can_update_booking_status(client: TestClient, admin_user):
    admin_token = get_token(client, "admin@test.com", "AdminPass123")
    slot_id = setup_service_slot(client, admin_token, capacity=1)

    client.post("/api/v1/auth/register", json={"full_name": "Customer C", "email": "custc@test.com", "password": "password123"})
    customer_token = get_token(client, "custc@test.com", "password123")

    booking = client.post(
        "/api/v1/bookings",
        json={"slot_id": slot_id, "reason": "Status test"},
        headers=auth_headers(customer_token),
    ).json()

    response = client.patch(
        f"/api/v1/admin/bookings/{booking['id']}/status",
        params={"new_status": "confirmed"},
        headers=auth_headers(admin_token),
    )
    assert response.status_code == 200
    assert response.json()["status"] == "confirmed"

    invalid = client.patch(
        f"/api/v1/admin/bookings/{booking['id']}/status",
        params={"new_status": "pending"},
        headers=auth_headers(admin_token),
    )
    assert invalid.status_code == 400