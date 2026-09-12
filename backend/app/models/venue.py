from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base, PKMixin, PublicIdMixin, TimestampMixin


class Venue(Base, PKMixin, PublicIdMixin, TimestampMixin):
    """A sports venue (manager-owned). Client key is `public_id` (UUIDv7)."""

    __tablename__ = "venues"

    name: Mapped[str] = mapped_column(String(120), nullable=False)
    address: Mapped[str] = mapped_column(String(255), nullable=False, default="")
