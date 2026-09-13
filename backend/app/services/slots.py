from datetime import date, datetime, time
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.config import settings
from app.models.court import Court
from app.models.slot import Slot
from app.schemas.slot import SlotCreate, SlotUpdate
from app.services import bookings as booking_service


def _court_id(db: Session, court_public_id: UUID) -> int | None:
    court = db.scalars(select(Court).where(Court.public_id == court_public_id)).first()
    return court.id if court else None


def list_slots(db: Session, court_public_id: UUID, day: date) -> list[Slot] | None:
    court_id = _court_id(db, court_public_id)
    if court_id is None:
        return None
    booking_service.expire_stale_bookings(db, settings.booking_ttl_minutes)
    start = datetime.combine(day, time.min)
    end = datetime.combine(day, time.max)
    stmt = (
        select(Slot)
        .where(Slot.court_id == court_id)
        .where(Slot.starts_at >= start, Slot.ends_at <= end)
        .order_by(Slot.starts_at)
    )
    return list(db.scalars(stmt).all())


def get_by_public_id(db: Session, public_id: UUID) -> Slot | None:
    return db.scalars(select(Slot).where(Slot.public_id == public_id)).first()


def create_slots(db: Session, items: list[SlotCreate]) -> list[Slot] | None:
    court_ids: dict[UUID, int] = {}
    rows: list[Slot] = []
    for item in items:
        if item.court_public_id not in court_ids:
            court_id = _court_id(db, item.court_public_id)
            if court_id is None:
                return None
            court_ids[item.court_public_id] = court_id
        rows.append(
            Slot(
                court_id=court_ids[item.court_public_id],
                starts_at=item.starts_at,
                ends_at=item.ends_at,
                price=item.price,
            )
        )
    db.add_all(rows)
    db.commit()
    for row in rows:
        db.refresh(row)
    return rows


def update_slot(db: Session, slot: Slot, data: SlotUpdate) -> Slot:
    if data.status is not None:
        slot.status = data.status
    if data.price is not None:
        slot.price = data.price
    db.commit()
    db.refresh(slot)
    return slot


def court_public_id(db: Session, slot: Slot) -> UUID:
    return db.get(Court, slot.court_id).public_id
