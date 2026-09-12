from sqlalchemy.orm import DeclarativeBase


class Base(DeclarativeBase):
    """Declarative base for all ORM models.

    Alembic imports this via `alembic/env.py` (through `app.models`).
    Domain models (Venue, Court, Slot, Booking, Payment) will subclass it.
    """
