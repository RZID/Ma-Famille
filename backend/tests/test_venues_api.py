from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

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


def test_venue_crud_roundtrip():
    client = _client()
    try:
        created = client.post(
            "/api/v1/venues", json={"name": "GOR A", "address": "Jakarta"}
        )
        assert created.status_code == 201, created.text
        public_id = created.json()["public_id"]

        listed = client.get("/api/v1/venues")
        assert len(listed.json()) == 1

        fetched = client.get(f"/api/v1/venues/{public_id}")
        assert fetched.json()["name"] == "GOR A"

        updated = client.patch(
            f"/api/v1/venues/{public_id}", json={"name": "GOR B"}
        )
        assert updated.json()["name"] == "GOR B"

        assert client.get("/api/v1/venues/00000000-0000-0000-0000-000000000000").status_code == 404

        assert client.delete(f"/api/v1/venues/{public_id}").status_code == 204
        assert client.get(f"/api/v1/venues/{public_id}").status_code == 404
    finally:
        app.dependency_overrides.pop(get_db, None)
