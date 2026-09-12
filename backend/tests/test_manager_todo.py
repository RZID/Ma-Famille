from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_manager_todo_routes_return_501():
    assert client.get("/api/v1/manager/bookings").status_code == 501
    assert (
        client.get(
            "/api/v1/manager/occupancy",
            params={"from_day": "2026-10-01", "to_day": "2026-10-07"},
        ).status_code
        == 501
    )


def test_manager_routes_in_openapi():
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/manager/bookings" in paths
    assert "/api/v1/manager/occupancy" in paths
