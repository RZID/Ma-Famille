"""Domain models.

Future iterations:
  payment.py -> Payment (FK -> Booking, deposit/paid)

Every model module must be imported here so Alembic autogenerate sees it.
"""

from app.db.base import Base
from app.models.booking import Booking
from app.models.court import Court
from app.models.slot import Slot
from app.models.venue import Venue

__all__ = ["Base", "Booking", "Court", "Slot", "Venue"]
