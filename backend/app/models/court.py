from sqlalchemy import Boolean, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, PKMixin, PublicIdMixin, TimestampMixin


class Court(Base, PKMixin, PublicIdMixin, TimestampMixin):
    """A bookable court inside a venue. Rates differ weekday vs weekend."""

    __tablename__ = "courts"

    venue_id: Mapped[int] = mapped_column(ForeignKey("venues.id"), nullable=False)
    name: Mapped[str] = mapped_column(String(120), nullable=False)
    sport: Mapped[str] = mapped_column(String(20), nullable=False)
    price_weekday: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    price_weekend: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
