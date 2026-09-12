"""Demo seed: 1 venue, 2 courts, 7 days of hourly slots, 1 booking.

Idempotent — exits quietly when the demo venue already exists.
Run: make db-seed (needs a live PostgreSQL + migrated schema).
"""

from datetime import date, datetime, time, timedelta

from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.booking import Booking
from app.models.court import Court
from app.models.slot import Slot
from app.models.venue import Venue

VENUE_NAME = "GOR Ma-Famille Demo"


def main() -> None:
    db = SessionLocal()
    try:
        if db.scalars(select(Venue).where(Venue.name == VENUE_NAME)).first():
            print("already seeded")
            return

        venue = Venue(name=VENUE_NAME, address="Jl. Demo No. 1")
        db.add(venue)
        db.flush()

        courts = [
            Court(
                venue_id=venue.id,
                name="Futsal A",
                sport="futsal",
                price_weekday=100000,
                price_weekend=150000,
            ),
            Court(
                venue_id=venue.id,
                name="Badminton 1",
                sport="badminton",
                price_weekday=50000,
                price_weekend=80000,
            ),
        ]
        db.add_all(courts)
        db.flush()

        today = date.today()
        for offset in range(7):
            day = today + timedelta(days=offset)
            weekend = day.weekday() >= 5
            for hour in range(8, 22):
                for court in courts:
                    price = court.price_weekend if weekend else court.price_weekday
                    db.add(
                        Slot(
                            court_id=court.id,
                            starts_at=datetime.combine(day, time(hour)),
                            ends_at=datetime.combine(day, time(hour + 1)),
                            price=price,
                        )
                    )
        db.flush()

        first_slot = db.scalars(select(Slot).order_by(Slot.id)).first()
        first_slot.status = "booked"
        db.add(
            Booking(
                slot_id=first_slot.id,
                customer_name="Demo User",
                customer_contact="0812000000",
                status="confirmed",
            )
        )
        db.commit()
        print("seeded", VENUE_NAME)
    finally:
        db.close()


if __name__ == "__main__":
    main()
