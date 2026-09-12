"""Lightweight access control.

Manager-only routes require `X-Manager-Token` matching MANAGER_TOKEN.
Empty MANAGER_TOKEN (local dev default) leaves routes open; production
sets it in backend/.env. Full user auth lands in a later iteration.
"""

import hmac

from fastapi import HTTPException, Security
from fastapi.security import APIKeyHeader

from app.core.config import settings

_scheme = APIKeyHeader(name="X-Manager-Token", auto_error=False)


def require_manager(token: str | None = Security(_scheme)) -> None:
    if not settings.manager_token:
        return
    if not token or not hmac.compare_digest(token, settings.manager_token):
        raise HTTPException(status_code=401, detail="manager token required")
