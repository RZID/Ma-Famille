"""Domain models.

Future iterations:
  court.py   -> Court (FK -> Venue)
  slot.py    -> Schedule/Slot (FK -> Court, start/end, price)
  booking.py -> Booking (FK -> Slot, customer, conflict guard)
  payment.py -> Payment (FK -> Booking, deposit/paid)

Every model module must be imported here so Alembic autogenerate sees it.
"""

from app.db.base import Base
from app.models.venue import Venue

__all__ = ["Base", "Venue"]
