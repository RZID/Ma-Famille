from datetime import date

from pydantic import BaseModel, Field


class OccupancyPoint(BaseModel):
    day: date
    total_slots: int = Field(ge=0)
    booked_slots: int = Field(ge=0)
    occupancy_rate: float = Field(ge=0, le=1)
