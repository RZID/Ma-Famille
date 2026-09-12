from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.booking import BookingCreate, BookingResponse
from app.services import bookings as booking_service

router = APIRouter(prefix="/bookings", tags=["bookings"])


def _to_response(db: Session, booking) -> BookingResponse:
    return BookingResponse(
        public_id=booking.public_id,
        slot_public_id=booking_service.slot_public_id(db, booking),
        customer_name=booking.customer_name,
        customer_contact=booking.customer_contact,
        status=booking.status,
        created_at=booking.created_at,
    )


@router.post(
    "",
    summary="Book a slot (409 on conflict)",
    status_code=201,
    responses={409: {"description": "Slot already booked"}},
)
def create_booking(body: BookingCreate, db: Session = Depends(get_db)) -> BookingResponse:
    try:
        booking = booking_service.create_booking(db, body)
    except IntegrityError:
        raise HTTPException(status_code=409, detail="slot already booked")
    if booking is None:
        raise HTTPException(status_code=404, detail="slot not found")
    return _to_response(db, booking)


@router.get("", summary="Customer booking history")
def list_my_bookings(customer_contact: str, db: Session = Depends(get_db)):
    bookings = booking_service.list_by_contact(db, customer_contact)
    return [_to_response(db, b) for b in bookings]


@router.get("/{public_id}", summary="Get booking")
def get_booking(public_id: UUID, db: Session = Depends(get_db)) -> BookingResponse:
    booking = booking_service.get_by_public_id(db, public_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="booking not found")
    return _to_response(db, booking)


@router.post("/{public_id}/confirm", summary="Confirm booking (deposit/manager)")
def confirm_booking(public_id: UUID, db: Session = Depends(get_db)) -> BookingResponse:
    booking = booking_service.get_by_public_id(db, public_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="booking not found")
    confirmed = booking_service.confirm_booking(db, booking)
    if confirmed is None:
        raise HTTPException(status_code=409, detail="booking is cancelled")
    return _to_response(db, confirmed)


@router.post("/{public_id}/cancel", summary="Cancel booking")
def cancel_booking(public_id: UUID, db: Session = Depends(get_db)) -> BookingResponse:
    booking = booking_service.get_by_public_id(db, public_id)
    if booking is None:
        raise HTTPException(status_code=404, detail="booking not found")
    return _to_response(db, booking_service.cancel_booking(db, booking))
