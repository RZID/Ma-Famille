from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.slot import Slot
from app.schemas.booking import BookingCreate


def _slot_id(db: Session, slot_public_id: UUID) -> int | None:
    slot = db.scalars(select(Slot).where(Slot.public_id == slot_public_id)).first()
    return slot.id if slot else None


def get_by_public_id(db: Session, public_id: UUID) -> Booking | None:
    return db.scalars(select(Booking).where(Booking.public_id == public_id)).first()


def list_by_contact(db: Session, customer_contact: str) -> list[Booking]:
    stmt = (
        select(Booking)
        .where(Booking.customer_contact == customer_contact)
        .order_by(Booking.id)
    )
    return list(db.scalars(stmt).all())


def create_booking(db: Session, data: BookingCreate) -> Booking | None:
    """Returns None when the slot is unknown; raises IntegrityError on conflict."""
    slot_id = _slot_id(db, data.slot_public_id)
    if slot_id is None:
        return None
    booking = Booking(
        slot_id=slot_id,
        customer_name=data.customer_name,
        customer_contact=data.customer_contact,
    )
    db.add(booking)
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise
    db.refresh(booking)
    return booking


def confirm_booking(db: Session, booking: Booking) -> Booking | None:
    if booking.status == "cancelled":
        return None
    booking.status = "confirmed"
    db.commit()
    db.refresh(booking)
    return booking


def cancel_booking(db: Session, booking: Booking) -> Booking:
    booking.status = "cancelled"
    db.commit()
    db.refresh(booking)
    return booking


def slot_public_id(db: Session, booking: Booking) -> UUID:
    return db.get(Slot, booking.slot_id).public_id
