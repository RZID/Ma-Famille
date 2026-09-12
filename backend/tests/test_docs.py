from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_openapi_json_lists_health_routes():
    res = client.get("/openapi.json")
    assert res.status_code == 200
    spec = res.json()
    assert spec["info"]["title"] == "ma-famille-api"
    paths = spec["paths"]
    assert "/api/v1/health" in paths
    assert "/api/v1/health/db" in paths


def test_swagger_ui_served():
    res = client.get("/docs")
    assert res.status_code == 200
    assert "swagger" in res.text.lower()


def test_redoc_served():
    res = client.get("/redoc")
    assert res.status_code == 200
