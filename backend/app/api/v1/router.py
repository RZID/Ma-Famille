from fastapi import APIRouter

from app.api.v1 import health

# Domain routers (Venue, Court, Slot, Booking, Payment) will be included here
# in follow-up iterations. Keep this file as the single v1 composition root.
router = APIRouter()
router.include_router(health.router, tags=["health"])
