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


def test_manager_bookings_and_occupancy():
    client = _client()
    try:
        venue = client.post("/v1/venues", json={"name": "GOR", "address": "Jkt"}).json()
        court = client.post(
            "/v1/courts",
            json={
                "venue_public_id": venue["public_id"],
                "name": "C1",
                "sport": "futsal",
                "price_weekday": 100000,
                "price_weekend": 150000,
            },
        ).json()
        slots = client.post(
            "/v1/slots",
            json=[
                {
                    "court_public_id": court["public_id"],
                    "starts_at": "2026-10-01T10:00:00",
                    "ends_at": "2026-10-01T11:00:00",
                    "price": 120000,
                },
                {
                    "court_public_id": court["public_id"],
                    "starts_at": "2026-10-01T11:00:00",
                    "ends_at": "2026-10-01T12:00:00",
                    "price": 120000,
                },
            ],
        ).json()
        booking = client.post(
            "/v1/bookings",
            json={
                "slot_public_id": slots[0]["public_id"],
                "customer_name": "Budi",
                "customer_contact": "0812",
            },
        ).json()

        all_bookings = client.get("/v1/manager/bookings")
        assert len(all_bookings.json()) == 1

        pending = client.get("/v1/manager/bookings", params={"booking_status": "pending"})
        assert len(pending.json()) == 1

        confirmed = client.get(
            "/v1/manager/bookings", params={"booking_status": "confirmed"}
        )
        assert confirmed.json() == []

        occ = client.get(
            "/v1/manager/occupancy",
            params={"from_day": "2026-10-01", "to_day": "2026-10-01"},
        ).json()
        assert occ[0]["total_slots"] == 2
        assert occ[0]["booked_slots"] == 1
        assert occ[0]["occupancy_rate"] == 0.5

        assert booking["status"] == "pending"
    finally:
        app.dependency_overrides.pop(get_db, None)
