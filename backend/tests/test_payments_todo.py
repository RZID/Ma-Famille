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
