from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
SAMPLE_ID = str(uuid4())


def test_venue_todo_routes_return_501():
    assert client.get("/api/v1/venues").status_code == 501
    assert (
        client.post("/api/v1/venues", json={"name": "GOR A"}).status_code == 501
    )
    assert client.get(f"/api/v1/venues/{SAMPLE_ID}").status_code == 501


def test_venue_routes_in_openapi():
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/venues" in paths
    assert "/api/v1/venues/{public_id}" in paths
