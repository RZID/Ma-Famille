from fastapi import APIRouter

from app.api.v1 import courts, health, venues

# Domain routers (Slot, Booking, Payment) land in follow-up iterations.
# Keep this file as the single v1 composition root.
router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(venues.router)
router.include_router(courts.router)
