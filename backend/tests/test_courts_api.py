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


def _venue(client):
    res = client.post("/v1/venues", json={"name": "GOR A", "address": "Jkt"})
    return res.json()["public_id"]


def test_court_crud_roundtrip():
    client = _client()
    try:
        venue_id = _venue(client)
        payload = {
            "venue_public_id": venue_id,
            "name": "Court A",
            "sport": "futsal",
            "price_weekday": 100000,
            "price_weekend": 150000,
        }
        created = client.post("/v1/courts", json=payload)
        assert created.status_code == 201, created.text
        body = created.json()
        assert body["venue_public_id"] == venue_id
        public_id = body["public_id"]

        filtered = client.get("/v1/courts", params={"venue_public_id": venue_id})
        assert len(filtered.json()) == 1

        updated = client.patch(
            f"/v1/courts/{public_id}", json={"price_weekday": 120000}
        )
        assert updated.json()["price_weekday"] == 120000

        assert client.delete(f"/v1/courts/{public_id}").status_code == 204
        assert client.get(f"/v1/courts/{public_id}").json()["is_active"] is False
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_court_rejects_unknown_venue():
    client = _client()
    try:
        res = client.post(
            "/v1/courts",
            json={
                "venue_public_id": "00000000-0000-0000-0000-000000000000",
                "name": "X",
                "sport": "futsal",
                "price_weekday": 1,
                "price_weekend": 1,
            },
        )
        assert res.status_code == 404
    finally:
        app.dependency_overrides.pop(get_db, None)
