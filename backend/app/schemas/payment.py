from datetime import datetime
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field

PaymentKind = Literal["deposit", "full"]
PaymentStatus = Literal["unpaid", "paid", "refunded"]


class PaymentCreate(BaseModel):
    booking_public_id: UUID
    amount: int = Field(ge=0)
    kind: PaymentKind = "deposit"


class PaymentResponse(BaseModel):
    public_id: UUID
    booking_public_id: UUID
    amount: int
    kind: PaymentKind
    status: PaymentStatus
    created_at: datetime


class PaymentInitiateResponse(BaseModel):
    invoice_number: str
    checkout_url: str
    token_id: str = ""
