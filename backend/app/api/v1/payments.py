from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.db.session import get_db
from app.models.booking import Booking
from app.schemas.payment import (
    DokuWebhookAck,
    PaymentCreate,
    PaymentInitiateResponse,
    PaymentResponse,
)
from app.services import doku
from app.services import payments as payment_service

router = APIRouter(prefix="/payments", tags=["payments"])

WEBHOOK_TARGET = "/api/v1/payments/webhook/doku"


def _to_response(db: Session, payment) -> PaymentResponse:
    return PaymentResponse(
        public_id=payment.public_id,
        booking_public_id=payment_service.booking_public_id(db, payment),
        amount=payment.amount,
        kind=payment.kind,
        status=payment.status,
        created_at=payment.created_at,
    )


@router.post(
    "",
    summary="Create DOKU checkout (sandbox)",
    response_model=PaymentInitiateResponse,
    responses={501: {"description": "DOKU keys missing"}},
)
def create_payment(body: PaymentCreate, db: Session = Depends(get_db)):
    booking = db.scalars(
        select(Booking).where(Booking.public_id == body.booking_public_id)
    ).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="booking not found")
    invoice_number = doku.new_invoice_number()
    try:
        result = doku.create_checkout(
            invoice_number=invoice_number,
            amount=body.amount,
            customer_name=booking.customer_name,
        )
    except doku.DokuError as exc:
        raise HTTPException(
            status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=str(exc)
        ) from exc
    payment_service.create_payment(
        db,
        booking_id=booking.id,
        amount=body.amount,
        kind=body.kind,
        invoice_number=invoice_number,
    )
    return PaymentInitiateResponse(
        invoice_number=result.invoice_number,
        checkout_url=result.checkout_url,
        token_id=result.token_id,
    )


@router.get("", summary="List payments per booking")
def list_payments(
    booking_public_id: UUID, db: Session = Depends(get_db)
) -> list[PaymentResponse]:
    booking = db.scalars(
        select(Booking).where(Booking.public_id == booking_public_id)
    ).first()
    if booking is None:
        raise HTTPException(status_code=404, detail="booking not found")
    payments = payment_service.list_by_booking_id(db, booking.id)
    return [_to_response(db, p) for p in payments]


@router.post("/{public_id}/mark-paid", summary="Mark payment paid (manager)")
def mark_paid(public_id: UUID, db: Session = Depends(get_db)) -> PaymentResponse:
    payment = payment_service.get_by_public_id(db, public_id)
    if payment is None:
        raise HTTPException(status_code=404, detail="payment not found")
    return _to_response(db, payment_service.mark_paid(db, payment))


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
async def doku_webhook(request: Request, db: Session = Depends(get_db)):
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
    payment = payment_service.get_by_invoice(db, invoice)
    if payment is None:
        raise HTTPException(status_code=404, detail="unknown invoice")
    if mapped == "paid":
        payment_service.mark_paid(db, payment)
    return DokuWebhookAck(
        invoice_number=invoice, payment_status=mapped, detail="matched"
    )
