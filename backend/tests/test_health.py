from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_returns_service_info():
    res = client.get("/")
    assert res.status_code == 200
    body = res.json()
    assert body["service"] == "ma-famille-api"
    assert "env" in body


def test_v1_health_returns_ok():
    res = client.get("/v1/health")
    assert res.status_code == 200
    assert res.json() == {"status": "ok", "service": "ma-famille-api"}
