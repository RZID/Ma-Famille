from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.venue import Venue
from app.schemas.venue import VenueCreate, VenueUpdate


def list_venues(db: Session) -> list[Venue]:
    return list(db.scalars(select(Venue).order_by(Venue.id)).all())


def get_by_public_id(db: Session, public_id: UUID) -> Venue | None:
    return db.scalars(select(Venue).where(Venue.public_id == public_id)).first()


def create_venue(db: Session, data: VenueCreate) -> Venue:
    venue = Venue(name=data.name, address=data.address)
    db.add(venue)
    db.commit()
    db.refresh(venue)
    return venue


def update_venue(db: Session, venue: Venue, data: VenueUpdate) -> Venue:
    if data.name is not None:
        venue.name = data.name
    if data.address is not None:
        venue.address = data.address
    db.commit()
    db.refresh(venue)
    return venue


def delete_venue(db: Session, venue: Venue) -> None:
    db.delete(venue)
    db.commit()
