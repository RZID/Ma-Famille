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


def _slot(client):
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
    slot = client.post(
        "/api/v1/slots",
        json=[
            {
                "court_public_id": court["public_id"],
                "starts_at": "2026-10-01T10:00:00",
                "ends_at": "2026-10-01T11:00:00",
                "price": 120000,
            }
        ],
    ).json()
    return slot[0]["public_id"]


def test_booking_flow_with_conflict():
    client = _client()
    try:
        slot_id = _slot(client)
        first = client.post(
            "/api/v1/bookings",
            json={
                "slot_public_id": slot_id,
                "customer_name": "Budi",
                "customer_contact": "0812",
            },
        )
        assert first.status_code == 201, first.text
        assert first.json()["status"] == "pending"
        public_id = first.json()["public_id"]

        second = client.post(
            "/api/v1/bookings",
            json={
                "slot_public_id": slot_id,
                "customer_name": "Ani",
                "customer_contact": "0813",
            },
        )
        assert second.status_code == 409
        assert second.json()["detail"] == "slot already booked"

        history = client.get("/api/v1/bookings", params={"customer_contact": "0812"})
        assert len(history.json()) == 1

        confirmed = client.post(f"/api/v1/bookings/{public_id}/confirm")
        assert confirmed.json()["status"] == "confirmed"

        cancelled = client.post(f"/api/v1/bookings/{public_id}/cancel")
        assert cancelled.json()["status"] == "cancelled"
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_booking_unknown_slot_is_404():
    client = _client()
    try:
        res = client.post(
            "/api/v1/bookings",
            json={
                "slot_public_id": "00000000-0000-0000-0000-000000000000",
                "customer_name": "Budi",
                "customer_contact": "0812",
            },
        )
        assert res.status_code == 404
    finally:
        app.dependency_overrides.pop(get_db, None)
