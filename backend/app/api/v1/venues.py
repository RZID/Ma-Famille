from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.venue import VenueCreate, VenueResponse, VenueUpdate

router = APIRouter(prefix="/venues", tags=["venues"])

_TODO = "TODO: venue store not wired yet"


@router.get("", summary="TODO: list venues", response_model=list[VenueResponse])
def list_venues() -> list[VenueResponse]:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.post(
    "",
    summary="TODO: create venue (manager)",
    response_model=VenueResponse,
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
def create_venue(_body: VenueCreate) -> VenueResponse:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.get("/{public_id}", summary="TODO: get venue", response_model=VenueResponse)
def get_venue(public_id: UUID) -> VenueResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )


@router.patch("/{public_id}", summary="TODO: update venue (manager)")
def update_venue(public_id: UUID, _body: VenueUpdate) -> VenueResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )


@router.delete(
    "/{public_id}",
    summary="TODO: delete venue (manager)",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
def delete_venue(public_id: UUID) -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )
