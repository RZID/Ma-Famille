from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.booking import BookingCreate, BookingResponse

router = APIRouter(prefix="/bookings", tags=["bookings"])

_TODO = "TODO: booking store not wired yet (incl. conflict check)"


@router.post(
    "",
    summary="TODO: book a slot (409 on conflict)",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
    responses={409: {"description": "Slot already booked"}},
)
def create_booking(_body: BookingCreate) -> BookingResponse:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.get("", summary="TODO: customer booking history")
def list_my_bookings(customer_contact: str) -> list[BookingResponse]:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.get("/{public_id}", summary="TODO: get booking")
def get_booking(public_id: UUID) -> BookingResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )


@router.post("/{public_id}/confirm", summary="TODO: confirm booking (deposit/manager)")
def confirm_booking(public_id: UUID) -> BookingResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )


@router.post("/{public_id}/cancel", summary="TODO: cancel booking")
def cancel_booking(public_id: UUID) -> BookingResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )
