from datetime import date

from fastapi import APIRouter, HTTPException, status

from app.schemas.booking import BookingResponse
from app.schemas.manager import OccupancyPoint

router = APIRouter(prefix="/manager", tags=["manager"])

_TODO = "TODO: manager queries not wired yet"


@router.get("/bookings", summary="TODO: incoming bookings (manager)")
def incoming_bookings(booking_status: str | None = None) -> list[BookingResponse]:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.get("/occupancy", summary="TODO: occupancy summary for chart (manager)")
def occupancy(from_day: date, to_day: date) -> list[OccupancyPoint]:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)
