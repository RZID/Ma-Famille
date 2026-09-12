from uuid import UUID

from fastapi import APIRouter, HTTPException, Request, status

from app.core.config import settings
from app.schemas.payment import (
    DokuWebhookAck,
    PaymentCreate,
    PaymentInitiateResponse,
    PaymentResponse,
)
from app.services import doku

router = APIRouter(prefix="/payments", tags=["payments"])

WEBHOOK_TARGET = "/api/v1/payments/webhook/doku"

_TODO = "TODO: payment store not wired yet (DOKU checkout is live in sandbox)"


@router.post(
    "",
    summary="Create DOKU checkout (sandbox)",
    response_model=PaymentInitiateResponse,
    responses={501: {"description": "DOKU keys missing or store not wired"}},
)
def create_payment(body: PaymentCreate) -> PaymentInitiateResponse:
    try:
        result = doku.create_checkout(
            invoice_number=doku.new_invoice_number(),
            amount=body.amount,
            customer_name="ma-famille customer",
        )
    except doku.DokuError as exc:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(exc)
        ) from exc
    return PaymentInitiateResponse(
        invoice_number=result.invoice_number,
        checkout_url=result.checkout_url,
        token_id=result.token_id,
    )


@router.get("", summary="TODO: list payments per booking")
def list_payments(booking_public_id: UUID) -> list[PaymentResponse]:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.post("/{public_id}/mark-paid", summary="TODO: mark payment paid (manager)")
def mark_paid(public_id: UUID) -> PaymentResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )


def _webhook_status(body: dict) -> tuple[str, str]:
    try:
        invoice = body["order"]["invoice_number"]
    except (KeyError, TypeError):
        raise HTTPException(status_code=422, detail="missing order.invoice_number")
    raw_status = ""
    try:
        raw_status = str(body["transaction"]["status"]).upper()
    except (KeyError, TypeError):
        pass
    if raw_status == "SUCCESS":
        mapped = "paid"
    elif raw_status in ("FAILED", "EXPIRED", "CANCELLED"):
        mapped = "failed"
    else:
        mapped = "pending"
    return invoice, mapped


@router.post(
    "/webhook/doku",
    summary="DOKU HTTP notification (sandbox)",
    response_model=DokuWebhookAck,
    responses={401: {"description": "Bad signature"}},
)
async def doku_webhook(request: Request) -> DokuWebhookAck:
    if not settings.doku_configured:
        raise HTTPException(status_code=501, detail="DOKU keys not configured")
    raw = await request.body()
    headers = request.headers
    ok = doku.verify_signature(
        signature=headers.get("signature", ""),
        client_id=headers.get("client-id", ""),
        request_id=headers.get("request-id", ""),
        timestamp=headers.get("request-timestamp", ""),
        request_target=WEBHOOK_TARGET,
        digest=doku.build_digest(raw),
        secret=settings.doku_secret_key,
    )
    if not ok:
        raise HTTPException(status_code=401, detail="bad DOKU signature")
    try:
        body = dict(await request.json())
    except ValueError:
        raise HTTPException(status_code=422, detail="invalid JSON body")
    invoice, mapped = _webhook_status(body)
    return DokuWebhookAck(invoice_number=invoice, payment_status=mapped)
