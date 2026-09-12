from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, PKMixin, PublicIdMixin, TimestampMixin


class Slot(Base, PKMixin, PublicIdMixin, TimestampMixin):
    """A bookable time window on a court.

    Status: available | held | booked | blocked.
    """

    __tablename__ = "slots"
    __table_args__ = (CheckConstraint("ends_at > starts_at", name="ck_slots_ends_after_starts"),)

    court_id: Mapped[int] = mapped_column(ForeignKey("courts.id"), nullable=False)
    starts_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    price: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="available")
