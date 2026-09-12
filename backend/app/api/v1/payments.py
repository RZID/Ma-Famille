from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.payment import PaymentCreate, PaymentResponse

router = APIRouter(prefix="/payments", tags=["payments"])

_TODO = "TODO: payment store not wired yet (no real gateway)"


@router.post("", summary="TODO: record deposit/full payment", status_code=501)
def create_payment(_body: PaymentCreate) -> PaymentResponse:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.get("", summary="TODO: list payments per booking")
def list_payments(booking_public_id: UUID) -> list[PaymentResponse]:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.post("/{public_id}/mark-paid", summary="TODO: mark payment paid (manager)")
def mark_paid(public_id: UUID) -> PaymentResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )
