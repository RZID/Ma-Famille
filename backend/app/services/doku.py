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
from datetime import datetime, timezone
from uuid import uuid4


def utc_timestamp() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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
