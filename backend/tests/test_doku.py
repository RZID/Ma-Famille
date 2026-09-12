import base64
import hashlib
import re

from app.services import doku

SECRET = "SK-test-123"
BODY = b'{"order":{"invoice_number":"INV-1","amount":50000}}'


def test_digest_matches_sha256():
    assert doku.build_digest(BODY) == base64.b64encode(hashlib.sha256(BODY).digest()).decode()


def test_signature_roundtrip_verifies():
    sig = doku.build_signature(
        client_id="MCH-1",
        request_id="req-1",
        timestamp="2026-09-12T00:00:00Z",
        request_target="/checkout/v1/payment",
        digest=doku.build_digest(BODY),
        secret=SECRET,
    )
    assert sig.startswith("HMACSHA256=")
    assert doku.verify_signature(
        signature=sig,
        client_id="MCH-1",
        request_id="req-1",
        timestamp="2026-09-12T00:00:00Z",
        request_target="/checkout/v1/payment",
        digest=doku.build_digest(BODY),
        secret=SECRET,
    )


def test_tampered_body_or_secret_fails():
    sig = doku.build_signature(
        client_id="MCH-1",
        request_id="req-1",
        timestamp="2026-09-12T00:00:00Z",
        request_target="/checkout/v1/payment",
        digest=doku.build_digest(BODY),
        secret=SECRET,
    )
    assert not doku.verify_signature(
        signature=sig,
        client_id="MCH-1",
        request_id="req-1",
        timestamp="2026-09-12T00:00:00Z",
        request_target="/checkout/v1/payment",
        digest=doku.build_digest(b'{"order":{"amount":1}}'),
        secret=SECRET,
    )
    assert not doku.verify_signature(
        signature=sig,
        client_id="MCH-1",
        request_id="req-1",
        timestamp="2026-09-12T00:00:00Z",
        request_target="/checkout/v1/payment",
        digest=doku.build_digest(BODY),
        secret="wrong",
    )


def test_timestamp_is_utc_iso8601():
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", doku.utc_timestamp())
