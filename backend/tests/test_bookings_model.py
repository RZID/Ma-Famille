from datetime import UTC, datetime, timedelta

from sqlalchemy import create_engine
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.booking import Booking
from app.models.court import Court
from app.models.slot import Slot
from app.models.venue import Venue


def _session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def _slot(db):
    venue = Venue(name="GOR A", address="Jakarta")
    db.add(venue)
    db.flush()
    court = Court(venue_id=venue.id, name="C1", sport="futsal")
    db.add(court)
    db.flush()
    slot = Slot(
        court_id=court.id,
        starts_at=datetime(2026, 10, 1, 10, 0),
        ends_at=datetime(2026, 10, 1, 11, 0),
    )
    db.add(slot)
    db.flush()
    return slot


def test_second_active_booking_on_same_slot_conflicts():
    db = _session()
    slot = _slot(db)
    db.add(Booking(slot_id=slot.id, customer_name="A", customer_contact="081"))
    db.commit()
    db.add(Booking(slot_id=slot.id, customer_name="B", customer_contact="082"))
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
    else:
        raise AssertionError("double booking should violate the partial index")


def test_cancelled_booking_frees_the_slot():
    db = _session()
    slot = _slot(db)
    db.add(
        Booking(
            slot_id=slot.id,
            customer_name="A",
            customer_contact="081",
            status="cancelled",
        )
    )
    db.commit()
    db.add(Booking(slot_id=slot.id, customer_name="B", customer_contact="082"))
    db.commit()


def test_stale_pending_booking_expires_and_frees_slot():
    from app.services.bookings import expire_stale_bookings

    db = _session()
    slot = _slot(db)
    booking = Booking(slot_id=slot.id, customer_name="A", customer_contact="081")
    db.add(booking)
    db.commit()
    booking.created_at = datetime.now(UTC).replace(tzinfo=None) - timedelta(hours=2)
    slot.status = "booked"
    db.commit()

    assert expire_stale_bookings(db, ttl_minutes=30) == 1
    db.refresh(booking)
    db.refresh(slot)
    assert booking.status == "cancelled"
    assert slot.status == "available"
    assert expire_stale_bookings(db, ttl_minutes=30) == 0
