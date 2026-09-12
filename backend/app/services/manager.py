from datetime import date, datetime, time, timedelta

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from app.models.booking import Booking
from app.models.slot import Slot


def incoming_bookings(db: Session, booking_status: str | None = None):
    stmt = select(Booking).order_by(Booking.id)
    if booking_status is not None:
        stmt = stmt.where(Booking.status == booking_status)
    return list(db.scalars(stmt).all())


def occupancy(db: Session, from_day: date, to_day: date) -> list[dict]:
    points: list[dict] = []
    day = from_day
    while day <= to_day:
        start = datetime.combine(day, time.min)
        end = datetime.combine(day, time.max)
        total = db.scalar(
            select(func.count())
            .select_from(Slot)
            .where(Slot.starts_at >= start, Slot.starts_at <= end)
        )
        booked = db.scalar(
            select(func.count(func.distinct(Booking.slot_id)))
            .select_from(Booking)
            .join(Slot, Slot.id == Booking.slot_id)
            .where(
                Slot.starts_at >= start,
                Slot.starts_at <= end,
                Booking.status != "cancelled",
            )
        )
        points.append(
            {
                "day": day,
                "total_slots": total,
                "booked_slots": booked,
                "occupancy_rate": (booked / total) if total else 0.0,
            }
        )
        day += timedelta(days=1)
    return points
