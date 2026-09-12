from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

BookingStatus = Literal["pending", "confirmed", "cancelled"]


class BookingCreate(BaseModel):
    slot_public_id: UUID
    customer_name: str = Field(min_length=1, max_length=120)
    customer_contact: str = Field(min_length=3, max_length=60)


class BookingResponse(BaseModel):
    public_id: UUID
    slot_public_id: UUID
    customer_name: str
    customer_contact: str
    status: BookingStatus
    created_at: datetime
