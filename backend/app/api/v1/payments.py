from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.payment import PaymentCreate, PaymentInitiateResponse, PaymentResponse
from app.services import doku

router = APIRouter(prefix="/payments", tags=["payments"])

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
