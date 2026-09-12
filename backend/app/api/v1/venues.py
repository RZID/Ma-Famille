from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.venue import VenueCreate, VenueResponse, VenueUpdate
from app.services import venues as venue_service

router = APIRouter(prefix="/venues", tags=["venues"])


def _to_response(venue) -> VenueResponse:
    return VenueResponse(
        public_id=venue.public_id,
        name=venue.name,
        address=venue.address,
        created_at=venue.created_at,
    )


@router.get("", summary="List venues", response_model=list[VenueResponse])
def list_venues(db: Session = Depends(get_db)) -> list[VenueResponse]:
    return [_to_response(v) for v in venue_service.list_venues(db)]


@router.post("", summary="Create venue (manager)", response_model=VenueResponse, status_code=201)
def create_venue(body: VenueCreate, db: Session = Depends(get_db)) -> VenueResponse:
    return _to_response(venue_service.create_venue(db, body))


@router.get("/{public_id}", summary="Get venue", response_model=VenueResponse)
def get_venue(public_id: UUID, db: Session = Depends(get_db)) -> VenueResponse:
    venue = venue_service.get_by_public_id(db, public_id)
    if venue is None:
        raise HTTPException(status_code=404, detail="venue not found")
    return _to_response(venue)


@router.patch("/{public_id}", summary="Update venue (manager)", response_model=VenueResponse)
def update_venue(
    public_id: UUID, body: VenueUpdate, db: Session = Depends(get_db)
) -> VenueResponse:
    venue = venue_service.get_by_public_id(db, public_id)
    if venue is None:
        raise HTTPException(status_code=404, detail="venue not found")
    return _to_response(venue_service.update_venue(db, venue, body))


@router.delete("/{public_id}", summary="Delete venue (manager)", status_code=204)
def delete_venue(public_id: UUID, db: Session = Depends(get_db)) -> None:
    venue = venue_service.get_by_public_id(db, public_id)
    if venue is None:
        raise HTTPException(status_code=404, detail="venue not found")
    venue_service.delete_venue(db, venue)
