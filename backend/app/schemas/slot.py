from datetime import date, datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

SlotStatus = Literal["available", "held", "booked", "blocked"]


class SlotCreate(BaseModel):
    court_public_id: UUID
    starts_at: datetime
    ends_at: datetime
    price: int = Field(ge=0)


class SlotUpdate(BaseModel):
    status: SlotStatus | None = None
    price: int | None = Field(default=None, ge=0)


class SlotResponse(BaseModel):
    public_id: UUID
    court_public_id: UUID
    starts_at: datetime
    ends_at: datetime
    price: int
    status: SlotStatus


class AvailabilityQuery(BaseModel):
    court_public_id: UUID
    day: date
