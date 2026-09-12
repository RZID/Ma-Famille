from fastapi import APIRouter

from app.api.v1 import bookings, courts, health, slots, venues

# Domain router (Payment) lands in the next iteration.
# Keep this file as the single v1 composition root.
router = APIRouter()
router.include_router(health.router, tags=["health"])
router.include_router(venues.router)
router.include_router(courts.router)
router.include_router(slots.router)
router.include_router(bookings.router)
