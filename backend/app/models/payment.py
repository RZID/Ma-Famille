from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, PKMixin, PublicIdMixin, TimestampMixin


class Payment(Base, PKMixin, PublicIdMixin, TimestampMixin):
    """A deposit or full payment for a booking.

    Kind: deposit | full. Status: unpaid | paid | refunded.
    No real gateway — DOKU sandbox drives transitions (see docs/PAYMENTS.md).
    """

    __tablename__ = "payments"

    booking_id: Mapped[int] = mapped_column(ForeignKey("bookings.id"), nullable=False)
    amount: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    kind: Mapped[str] = mapped_column(String(20), nullable=False, default="deposit")
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="unpaid")
