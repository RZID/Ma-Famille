from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app


def _client():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    TestingSession = sessionmaker(bind=engine)

    def override():
        db = TestingSession()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override
    return TestClient(app)


def test_manager_routes_open_without_token_by_default():
    client = _client()
    try:
        assert client.get("/api/v1/manager/bookings").status_code == 200
        assert client.get("/api/v1/venues").status_code == 200
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_manager_routes_locked_with_token_set(monkeypatch):
    client = _client()
    monkeypatch.setattr(settings, "manager_token", "s3cret")
    try:
        assert client.get("/api/v1/manager/bookings").status_code == 401
        # customer reads stay open, manager writes need the header
        assert client.get("/api/v1/venues").status_code == 200
        denied = client.post("/api/v1/venues", json={"name": "X"})
        assert denied.status_code == 401
        allowed = client.post(
            "/api/v1/venues", json={"name": "X"}, headers={"X-Manager-Token": "s3cret"}
        )
        assert allowed.status_code == 201
    finally:
        app.dependency_overrides.pop(get_db, None)
