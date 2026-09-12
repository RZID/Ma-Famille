from uuid import uuid4

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)
SAMPLE_ID = str(uuid4())


def test_payment_todo_routes_return_501():
    assert (
        client.post(
            "/api/v1/payments",
            json={"booking_public_id": SAMPLE_ID, "amount": 50000, "kind": "deposit"},
        ).status_code
        == 501
    )
    assert (
        client.post(f"/api/v1/payments/{SAMPLE_ID}/mark-paid").status_code == 501
    )


def test_payment_routes_in_openapi():
    paths = client.get("/openapi.json").json()["paths"]
    assert "/api/v1/payments" in paths


def test_checkout_passthrough_when_doku_mocked(monkeypatch):
    from app.api.v1 import payments
    from app.services.doku import CheckoutResult

    def fake_checkout(**kwargs):
        assert kwargs["amount"] == 50000
        return CheckoutResult(
            invoice_number="MAF-TEST", checkout_url="https://pay.test/x", token_id="tok"
        )

    monkeypatch.setattr(payments.doku, "create_checkout", fake_checkout)
    res = client.post(
        "/api/v1/payments",
        json={"booking_public_id": SAMPLE_ID, "amount": 50000, "kind": "deposit"},
    )
    assert res.status_code == 200
    assert res.json()["checkout_url"] == "https://pay.test/x"


WEBHOOK_PATH = "/api/v1/payments/webhook/doku"


def test_webhook_verifies_signature_and_maps_status(monkeypatch):
    import json

    from app.api.v1 import payments
    from app.core.config import settings
    from app.services import doku

    monkeypatch.setattr(settings, "doku_client_id", "MCH-TEST")
    monkeypatch.setattr(settings, "doku_secret_key", "secret-test")

    def signed_post(payload: dict, secret="secret-test"):
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

    ok_body = {
        "order": {"invoice_number": "MAF-1", "amount": 50000},
        "transaction": {"status": "SUCCESS"},
    }
    res = signed_post(ok_body)
    assert res.status_code == 200, res.text
    assert res.json()["payment_status"] == "paid"

    res = signed_post(ok_body, secret="wrong")
    assert res.status_code == 401
