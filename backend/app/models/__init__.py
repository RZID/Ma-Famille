"""Domain models (planned).

Future iterations:
  venue.py   -> Venue
  court.py   -> Court (FK -> Venue)
  slot.py    -> Schedule/Slot (FK -> Court, start/end, price)
  booking.py -> Booking (FK -> Slot, customer, conflict guard)
  payment.py -> Payment (FK -> Booking, deposit/paid)

Import Base here so Alembic sees metadata via `app.models`:
  from app.db.base import Base
"""

from app.db.base import Base

__all__ = ["Base"]
