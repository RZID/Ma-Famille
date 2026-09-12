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


def _court(client):
    venue = client.post("/api/v1/venues", json={"name": "GOR", "address": "Jkt"}).json()
    court = client.post(
        "/api/v1/courts",
        json={
            "venue_public_id": venue["public_id"],
            "name": "C1",
            "sport": "futsal",
            "price_weekday": 100000,
            "price_weekend": 150000,
        },
    ).json()
    return court["public_id"]


def test_slot_availability_roundtrip():
    client = _client()
    try:
        court_id = _court(client)
        payload = [
            {
                "court_public_id": court_id,
                "starts_at": "2026-10-01T10:00:00",
                "ends_at": "2026-10-01T11:00:00",
                "price": 120000,
            },
            {
                "court_public_id": court_id,
                "starts_at": "2026-10-01T11:00:00",
                "ends_at": "2026-10-01T12:00:00",
                "price": 120000,
            },
        ]
        created = client.post("/api/v1/slots", json=payload)
        assert created.status_code == 201, created.text
        assert len(created.json()) == 2
        first_id = created.json()[0]["public_id"]

        day = client.get(
            "/api/v1/slots", params={"court_public_id": court_id, "day": "2026-10-01"}
        )
        assert len(day.json()) == 2

        other = client.get(
            "/api/v1/slots", params={"court_public_id": court_id, "day": "2026-10-02"}
        )
        assert other.json() == []

        blocked = client.patch(f"/api/v1/slots/{first_id}", json={"status": "blocked"})
        assert blocked.json()["status"] == "blocked"
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_slot_rejects_bad_range_and_unknown_court():
    client = _client()
    try:
        court_id = _court(client)
        bad = client.post(
            "/api/v1/slots",
            json=[
                {
                    "court_public_id": court_id,
                    "starts_at": "2026-10-01T12:00:00",
                    "ends_at": "2026-10-01T11:00:00",
                    "price": 1,
                }
            ],
        )
        assert bad.status_code == 422

        missing = client.get(
            "/api/v1/slots",
            params={
                "court_public_id": "00000000-0000-0000-0000-000000000000",
                "day": "2026-10-01",
            },
        )
        assert missing.status_code == 404
    finally:
        app.dependency_overrides.pop(get_db, None)
