from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
SAMPLE_ID = str(uuid4())


def test_slot_todo_routes_return_501():
    res = client.get(
        "/api/v1/slots", params={"court_public_id": SAMPLE_ID, "day": "2026-10-01"}
    )
    assert res.status_code == 501
    assert client.get(f"/api/v1/slots/{SAMPLE_ID}").status_code == 501


def test_slot_routes_in_openapi():
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/slots" in paths
    assert "/api/v1/slots/{public_id}" in paths
