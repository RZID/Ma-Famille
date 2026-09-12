from datetime import date
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import require_manager
from app.db.session import get_db
from app.schemas.slot import SlotCreate, SlotResponse, SlotUpdate
from app.services import slots as slot_service

router = APIRouter(prefix="/slots", tags=["slots"])


def _to_response(db: Session, slot) -> SlotResponse:
    return SlotResponse(
        public_id=slot.public_id,
        court_public_id=slot_service.court_public_id(db, slot),
        starts_at=slot.starts_at,
        ends_at=slot.ends_at,
        price=slot.price,
        status=slot.status,
    )


@router.get("", summary="Availability calendar per court per day")
def list_slots(
    court_public_id: UUID, day: date, db: Session = Depends(get_db)
) -> list[SlotResponse]:
    slots = slot_service.list_slots(db, court_public_id, day)
    if slots is None:
        raise HTTPException(status_code=404, detail="court not found")
    return [_to_response(db, s) for s in slots]


@router.post(
    "",
    summary="Create slots (manager)",
    status_code=201,
    dependencies=[Depends(require_manager)],
)
def create_slots(
    body: list[SlotCreate], db: Session = Depends(get_db)
) -> list[SlotResponse]:
    slots = slot_service.create_slots(db, body)
    if slots is None:
        raise HTTPException(status_code=404, detail="court not found")
    return [_to_response(db, s) for s in slots]


@router.get("/{public_id}", summary="Get slot")
def get_slot(public_id: UUID, db: Session = Depends(get_db)) -> SlotResponse:
    slot = slot_service.get_by_public_id(db, public_id)
    if slot is None:
        raise HTTPException(status_code=404, detail="slot not found")
    return _to_response(db, slot)


@router.patch(
    "/{public_id}",
    summary="Open/close slot (manager)",
    dependencies=[Depends(require_manager)],
)
def update_slot(
    public_id: UUID, body: SlotUpdate, db: Session = Depends(get_db)
) -> SlotResponse:
    slot = slot_service.get_by_public_id(db, public_id)
    if slot is None:
        raise HTTPException(status_code=404, detail="slot not found")
    return _to_response(db, slot_service.update_slot(db, slot, body))
