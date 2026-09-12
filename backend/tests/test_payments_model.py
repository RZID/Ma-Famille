from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.booking import Booking
from app.models.court import Court
from app.models.payment import Payment
from app.models.slot import Slot
from app.models.venue import Venue


def _session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_payment_defaults_to_unpaid_deposit():
    db = _session()
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
    booking = Booking(slot_id=slot.id, customer_name="A", customer_contact="081")
    db.add(booking)
    db.flush()

    payment = Payment(booking_id=booking.id, amount=50000)
    db.add(payment)
    db.commit()
    db.refresh(payment)
    assert payment.kind == "deposit"
    assert payment.status == "unpaid"
    assert payment.booking_id == booking.id
