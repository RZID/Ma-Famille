from datetime import datetime
from uuid import UUID

from sqlalchemy import BigInteger, DateTime, Uuid, func
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column

from app.core.ids import uuid7


class Base(DeclarativeBase):
    """Declarative base for all ORM models.

    Alembic imports this via `alembic/env.py` (through `app.models`).
    Domain models (Venue, Court, Slot, Booking, Payment) will subclass it.
    """


class PKMixin:
    """System-level PK: autoincrement integer, internal use (FKs/joins)."""

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)


class PublicIdMixin:
    """Client-facing id: UUIDv7, unique + indexed, safe to expose."""

    public_id: Mapped[UUID] = mapped_column(
        Uuid,
        unique=True,
        index=True,
        nullable=False,
        default=uuid7,
    )


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
