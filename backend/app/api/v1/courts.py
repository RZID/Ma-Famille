from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.security import require_manager
from app.db.session import get_db
from app.schemas.court import CourtCreate, CourtResponse, CourtUpdate
from app.services import courts as court_service

router = APIRouter(prefix="/courts", tags=["courts"])


def _to_response(db: Session, court) -> CourtResponse:
    return CourtResponse(
        public_id=court.public_id,
        venue_public_id=court_service.venue_public_id(db, court),
        name=court.name,
        sport=court.sport,
        price_weekday=court.price_weekday,
        price_weekend=court.price_weekend,
        is_active=court.is_active,
        created_at=court.created_at,
    )


@router.get("", summary="List courts (filter by venue)")
def list_courts(
    venue_public_id: UUID | None = None, db: Session = Depends(get_db)
) -> list[CourtResponse]:
    courts = court_service.list_courts(db, venue_public_id)
    return [_to_response(db, c) for c in courts]


@router.post(
    "",
    summary="Create court (manager)",
    status_code=201,
    dependencies=[Depends(require_manager)],
)
def create_court(body: CourtCreate, db: Session = Depends(get_db)) -> CourtResponse:
    court = court_service.create_court(db, body)
    if court is None:
        raise HTTPException(status_code=404, detail="venue not found")
    return _to_response(db, court)


@router.get("/{public_id}", summary="Get court")
def get_court(public_id: UUID, db: Session = Depends(get_db)) -> CourtResponse:
    court = court_service.get_by_public_id(db, public_id)
    if court is None:
        raise HTTPException(status_code=404, detail="court not found")
    return _to_response(db, court)


@router.patch(
    "/{public_id}",
    summary="Update court pricing (manager)",
    dependencies=[Depends(require_manager)],
)
def update_court(
    public_id: UUID, body: CourtUpdate, db: Session = Depends(get_db)
) -> CourtResponse:
    court = court_service.get_by_public_id(db, public_id)
    if court is None:
        raise HTTPException(status_code=404, detail="court not found")
    return _to_response(db, court_service.update_court(db, court, body))


@router.delete(
    "/{public_id}",
    summary="Deactivate court (manager)",
    status_code=204,
    dependencies=[Depends(require_manager)],
)
def delete_court(public_id: UUID, db: Session = Depends(get_db)) -> None:
    court = court_service.get_by_public_id(db, public_id)
    if court is None:
        raise HTTPException(status_code=404, detail="court not found")
    court_service.deactivate_court(db, court)
