from datetime import date
from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.slot import SlotCreate, SlotResponse, SlotUpdate

router = APIRouter(prefix="/slots", tags=["slots"])

_TODO = "TODO: slot store not wired yet"


@router.get("", summary="TODO: availability calendar per court per day")
def list_slots(court_public_id: UUID, day: date) -> list[SlotResponse]:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.post(
    "",
    summary="TODO: create slots (manager)",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
def create_slots(_body: list[SlotCreate]) -> list[SlotResponse]:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.get("/{public_id}", summary="TODO: get slot")
def get_slot(public_id: UUID) -> SlotResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )


@router.patch("/{public_id}", summary="TODO: open/close slot (manager)")
def update_slot(public_id: UUID, _body: SlotUpdate) -> SlotResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )
