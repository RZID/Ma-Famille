from datetime import datetime
from uuid import UUID

from pydantic import BaseModel, Field


class VenueCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    address: str = Field(default="", max_length=255)


class VenueUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    address: str | None = Field(default=None, max_length=255)


class VenueResponse(BaseModel):
    public_id: UUID
    name: str
    address: str
    created_at: datetime
