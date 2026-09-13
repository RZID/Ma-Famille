import json

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.api.v1 import payments
from app.core.config import settings
from app.db.base import Base
from app.db.session import get_db
from app.main import app
from app.services import doku
from app.services.doku import CheckoutResult

WEBHOOK_PATH = "/v1/payments/webhook/doku"


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


def _booking(client):
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
    slot = client.post(
        "/v1/slots",
        json=[
            {
                "court_public_id": court["public_id"],
                "starts_at": "2026-10-01T10:00:00",
                "ends_at": "2026-10-01T11:00:00",
                "price": 120000,
            }
        ],
    ).json()
    booking = client.post(
        "/v1/bookings",
        json={
            "slot_public_id": slot[0]["public_id"],
            "customer_name": "Budi",
            "customer_contact": "0812",
        },
    ).json()
    return booking["public_id"]


def _signed_post(client, payload, secret="secret-test"):
    raw = json.dumps(payload, separators=(",", ":")).encode()
    headers = {
        "Client-Id": "MCH-TEST",
        "Request-Id": "req-1",
        "Request-Timestamp": "2026-09-12T00:00:00Z",
        "Signature": doku.build_signature(
            client_id="MCH-TEST",
            request_id="req-1",
            timestamp="2026-09-12T00:00:00Z",
            request_target=payments.WEBHOOK_TARGET,
            digest=doku.build_digest(raw),
            secret=secret,
        ),
    }
    return client.post(WEBHOOK_PATH, content=raw, headers=headers)


def test_payment_checkout_and_mark_paid_auto_confirms(monkeypatch):
    client = _client()
    try:
        booking_id = _booking(client)

        def fake_checkout(**kwargs):
            return CheckoutResult(
                invoice_number=kwargs["invoice_number"],
                checkout_url="https://pay.test/x",
                token_id="tok",
            )

        monkeypatch.setattr(payments.doku, "create_checkout", fake_checkout)
        created = client.post(
            "/v1/payments",
            json={"booking_public_id": booking_id, "amount": 50000, "kind": "deposit"},
        )
        assert created.status_code == 200, created.text
        invoice = created.json()["invoice_number"]

        listed = client.get("/v1/payments", params={"booking_public_id": booking_id})
        assert len(listed.json()) == 1
        assert listed.json()[0]["status"] == "unpaid"
        public_id = listed.json()[0]["public_id"]

        paid = client.post(f"/v1/payments/{public_id}/mark-paid")
        assert paid.json()["status"] == "paid"

        booking = client.get(f"/v1/bookings/{booking_id}")
        assert booking.json()["status"] == "confirmed"

        monkeypatch.setattr(settings, "doku_client_id", "MCH-TEST")
        monkeypatch.setattr(settings, "doku_secret_key", "secret-test")
        res = _signed_post(
            client,
            {
                "order": {"invoice_number": invoice, "amount": 50000},
                "transaction": {"status": "SUCCESS"},
            },
        )
        assert res.status_code == 200
        assert res.json()["payment_status"] == "paid"
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_payment_without_keys_is_501():
    client = _client()
    try:
        booking_id = _booking(client)
        res = client.post(
            "/v1/payments",
            json={"booking_public_id": booking_id, "amount": 50000, "kind": "deposit"},
        )
        assert res.status_code == 501
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_webhook_rejects_bad_signature(monkeypatch):
    client = _client()
    try:
        monkeypatch.setattr(settings, "doku_client_id", "MCH-TEST")
        monkeypatch.setattr(settings, "doku_secret_key", "secret-test")
        res = _signed_post(
            client,
            {"order": {"invoice_number": "MAF-X", "amount": 1}},
            secret="wrong",
        )
        assert res.status_code == 401
    finally:
        app.dependency_overrides.pop(get_db, None)
