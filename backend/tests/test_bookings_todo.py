from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
SAMPLE_ID = str(uuid4())


def test_booking_todo_routes_return_501():
    assert (
        client.post(
            "/api/v1/bookings",
            json={
                "slot_public_id": SAMPLE_ID,
                "customer_name": "Budi",
                "customer_contact": "0812",
            },
        ).status_code
        == 501
    )
    assert client.get(f"/api/v1/bookings/{SAMPLE_ID}").status_code == 501
    assert (
        client.post(f"/api/v1/bookings/{SAMPLE_ID}/confirm").status_code == 501
    )


def test_booking_routes_in_openapi():
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/bookings" in paths
    assert "/api/v1/bookings/{public_id}" in paths
