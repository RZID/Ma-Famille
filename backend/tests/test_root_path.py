from fastapi.testclient import TestClient

from app.core.config import settings
from app.main import create_app


def test_subpath_routing_with_root_path(monkeypatch):
    monkeypatch.setattr(settings, "root_path", "/ma-famille")
    client = TestClient(create_app())
    assert client.get("/ma-famille/api/v1/health").status_code == 200
    assert client.get("/ma-famille/docs").status_code == 200
