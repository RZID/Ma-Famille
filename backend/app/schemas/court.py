from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

Sport = Literal["futsal", "badminton"]


class CourtCreate(BaseModel):
    venue_public_id: UUID
    name: str = Field(min_length=1, max_length=120)
    sport: Sport
    price_weekday: int = Field(ge=0)
    price_weekend: int = Field(ge=0)


class CourtUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    price_weekday: int | None = Field(default=None, ge=0)
    price_weekend: int | None = Field(default=None, ge=0)
    is_active: bool | None = None


class CourtResponse(BaseModel):
    public_id: UUID
    venue_public_id: UUID
    name: str
    sport: Sport
    price_weekday: int
    price_weekend: int
    is_active: bool
    created_at: datetime
