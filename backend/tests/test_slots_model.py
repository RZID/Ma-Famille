from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.court import Court
from app.models.slot import Slot
from app.models.venue import Venue


def _session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_slot_defaults_to_available_and_validates_range():
    from sqlalchemy.exc import IntegrityError

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
        price=120000,
    )
    db.add(slot)
    db.commit()
    db.refresh(slot)
    assert slot.status == "available"

    db.add(
        Slot(
            court_id=court.id,
            starts_at=datetime(2026, 10, 1, 12, 0),
            ends_at=datetime(2026, 10, 1, 11, 0),
        )
    )
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
    else:
        raise AssertionError("ends_at <= starts_at should violate the check")
