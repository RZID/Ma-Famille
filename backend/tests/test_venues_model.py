from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.db.base import Base
from app.models.venue import Venue


def _session():
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    Base.metadata.create_all(engine)
    return sessionmaker(bind=engine)()


def test_venue_gets_autoincrement_id_and_uuid7_public_id():
    db = _session()
    venue = Venue(name="GOR Senayan", address="Jakarta")
    db.add(venue)
    db.commit()
    db.refresh(venue)
    assert venue.id == 1
    assert venue.public_id.version == 7
    assert venue.created_at is not None


def test_venue_is_registered_in_metadata():
    assert "venues" in Base.metadata.tables
    cols = Base.metadata.tables["venues"].columns
    assert set(cols.keys()) >= {"id", "public_id", "name", "address"}
