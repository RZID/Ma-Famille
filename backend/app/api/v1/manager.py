from datetime import date

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.booking import BookingResponse
from app.schemas.manager import OccupancyPoint
from app.services import bookings as booking_service
from app.services import manager as manager_service

router = APIRouter(prefix="/manager", tags=["manager"])


@router.get("/bookings", summary="Incoming bookings (manager)")
def incoming_bookings(
    booking_status: str | None = None, db: Session = Depends(get_db)
):
    bookings = manager_service.incoming_bookings(db, booking_status)
    return [
        BookingResponse(
            public_id=b.public_id,
            slot_public_id=booking_service.slot_public_id(db, b),
            customer_name=b.customer_name,
            customer_contact=b.customer_contact,
            status=b.status,
            created_at=b.created_at,
        )
        for b in bookings
    ]


@router.get("/occupancy", summary="Occupancy summary for chart (manager)")
def occupancy(
    from_day: date, to_day: date, db: Session = Depends(get_db)
) -> list[OccupancyPoint]:
    if to_day < from_day:
        raise HTTPException(status_code=422, detail="to_day before from_day")
    if (to_day - from_day).days > 93:
        raise HTTPException(status_code=422, detail="range too wide (max 93 days)")
    return [
        OccupancyPoint(**point)
        for point in manager_service.occupancy(db, from_day, to_day)
    ]
