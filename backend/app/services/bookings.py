from datetime import UTC, datetime, timedelta
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.booking import Booking
from app.models.slot import Slot
from app.schemas.booking import BookingCreate


class SlotUnavailable(RuntimeError):
    pass


def expire_stale_bookings(db: Session, ttl_minutes: int) -> int:
    """Cancel pending bookings older than TTL and free their slots.

    Runs lazily inside read/write paths (no cron needed). Compares in
    Python so SQLite and Postgres timestamp flavors both behave.
    """
    now = datetime.now(UTC).replace(tzinfo=None)
    stale = db.scalars(select(Booking).where(Booking.status == "pending")).all()
    expired = 0
    for booking in stale:
        created = booking.created_at
        if created.tzinfo is not None:
            created = created.replace(tzinfo=None)
        if now - created > timedelta(minutes=ttl_minutes):
            booking.status = "cancelled"
            slot = db.get(Slot, booking.slot_id)
            if slot is not None and slot.status == "booked":
                slot.status = "available"
            expired += 1
    if expired:
        db.commit()
    return expired


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
    slot = db.scalars(select(Slot).where(Slot.public_id == data.slot_public_id)).first()
    if slot is None:
        return None
    expire_stale_bookings(db, settings.booking_ttl_minutes)
    db.refresh(slot)
    if slot.status != "available":
        raise SlotUnavailable(f"slot is {slot.status}")
    booking = Booking(
        slot_id=slot.id,
        customer_name=data.customer_name,
        customer_contact=data.customer_contact,
    )
    slot.status = "booked"
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
    slot = db.get(Slot, booking.slot_id)
    if slot is not None and slot.status == "booked":
        slot.status = "available"
    db.commit()
    db.refresh(booking)
    return booking


def slot_public_id(db: Session, booking: Booking) -> UUID:
    return db.get(Slot, booking.slot_id).public_id
