"""DOKU non-SNAP signature helpers (Checkout + HTTP Notification).

Spec: developers.doku.com — headers `Client-Id`, `Request-Id`,
`Request-Timestamp` (UTC ISO8601), `Signature: HMACSHA256=<base64>`.
Component string joins the five parts with "\\n"; Digest is
base64(SHA-256(minified JSON body)). Notifications from DOKU use the
merchant Notification URL path as Request-Target.
"""

import base64
import hashlib
import hmac
import json
from dataclasses import dataclass
from datetime import UTC, datetime
from uuid import uuid4

import httpx

from app.core.config import settings
from app.core.ids import uuid7


def utc_timestamp() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%dT%H:%M:%SZ")


def new_request_id() -> str:
    return str(uuid4())


def build_digest(body: bytes) -> str:
    return base64.b64encode(hashlib.sha256(body).digest()).decode()


def build_signature(
    *,
    client_id: str,
    request_id: str,
    timestamp: str,
    request_target: str,
    digest: str,
    secret: str,
) -> str:
    components = (
        f"Client-Id:{client_id}\n"
        f"Request-Id:{request_id}\n"
        f"Request-Timestamp:{timestamp}\n"
        f"Request-Target:{request_target}\n"
        f"Digest:{digest}"
    )
    mac = hmac.new(secret.encode(), components.encode(), hashlib.sha256).digest()
    return "HMACSHA256=" + base64.b64encode(mac).decode()


def verify_signature(
    *,
    signature: str,
    client_id: str,
    request_id: str,
    timestamp: str,
    request_target: str,
    digest: str,
    secret: str,
) -> bool:
    expected = build_signature(
        client_id=client_id,
        request_id=request_id,
        timestamp=timestamp,
        request_target=request_target,
        digest=digest,
        secret=secret,
    )
    return hmac.compare_digest(expected, signature)


CHECKOUT_TARGET = "/checkout/v1/payment"


class DokuError(RuntimeError):
    pass


@dataclass
class CheckoutResult:
    invoice_number: str
    checkout_url: str
    token_id: str


def new_invoice_number() -> str:
    return "MAF-" + uuid7().hex.upper()[:20]


def create_checkout(
    *, invoice_number: str, amount: int, customer_name: str, callback_url: str = ""
) -> CheckoutResult:
    """Create a DOKU hosted checkout page (sandbox by default).

    Raises DokuError when keys are missing or DOKU rejects the request.
    """
    if not settings.doku_configured:
        raise DokuError("DOKU keys not configured (see docs/PAYMENTS.md)")
    body = {
        "order": {"invoice_number": invoice_number, "amount": amount},
        "payment": {"payment_due_date": 60},
        "customer": {"name": customer_name},
    }
    if callback_url:
        body["order"]["callback_url"] = callback_url
    raw = json.dumps(body, separators=(",", ":")).encode()
    timestamp = utc_timestamp()
    request_id = new_request_id()
    headers = {
        "Client-Id": settings.doku_client_id,
        "Request-Id": request_id,
        "Request-Timestamp": timestamp,
        "Signature": build_signature(
            client_id=settings.doku_client_id,
            request_id=request_id,
            timestamp=timestamp,
            request_target=CHECKOUT_TARGET,
            digest=build_digest(raw),
            secret=settings.doku_secret_key,
        ),
    }
    try:
        res = httpx.post(
            settings.doku_base_url + CHECKOUT_TARGET,
            content=raw,
            headers=headers,
            timeout=15,
        )
    except httpx.HTTPError as exc:
        raise DokuError(f"DOKU request failed: {exc}") from exc
    if res.status_code != 200:
        raise DokuError(f"DOKU rejected checkout: HTTP {res.status_code}")
    try:
        payment = res.json()["response"]["payment"]
        return CheckoutResult(
            invoice_number=invoice_number,
            checkout_url=payment["url"],
            token_id=payment.get("token_id", ""),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise DokuError("DOKU returned an unexpected body") from exc
