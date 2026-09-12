from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
SAMPLE_ID = str(uuid4())


def test_court_todo_routes_return_501():
    assert client.get("/api/v1/courts").status_code == 501
    assert (
        client.post(
            "/api/v1/courts",
            json={
                "venue_public_id": SAMPLE_ID,
                "name": "Court A",
                "sport": "futsal",
                "price_weekday": 100000,
                "price_weekend": 150000,
            },
        ).status_code
        == 501
    )
    assert client.get(f"/api/v1/courts/{SAMPLE_ID}").status_code == 501


def test_court_routes_in_openapi():
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/courts" in paths
    assert "/api/v1/courts/{public_id}" in paths
