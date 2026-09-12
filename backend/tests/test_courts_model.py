from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.court import Court
from app.models.venue import Venue


def _session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_court_links_to_venue_and_defaults_active():
    db = _session()
    venue = Venue(name="GOR A", address="Jakarta")
    db.add(venue)
    db.flush()
    court = Court(
        venue_id=venue.id,
        name="Court 1",
        sport="futsal",
        price_weekday=100000,
        price_weekend=150000,
    )
    db.add(court)
    db.commit()
    db.refresh(court)
    assert court.id == 1
    assert court.public_id.version == 7
    assert court.is_active is True
    assert court.venue_id == venue.id
