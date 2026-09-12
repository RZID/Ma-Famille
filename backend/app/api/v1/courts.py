from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.schemas.court import CourtCreate, CourtResponse, CourtUpdate

router = APIRouter(prefix="/courts", tags=["courts"])

_TODO = "TODO: court store not wired yet"


@router.get("", summary="TODO: list courts (filter by venue)")
def list_courts(venue_public_id: UUID | None = None) -> list[CourtResponse]:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.post(
    "",
    summary="TODO: create court (manager)",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
def create_court(_body: CourtCreate) -> CourtResponse:
    raise HTTPException(status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=_TODO)


@router.get("/{public_id}", summary="TODO: get court")
def get_court(public_id: UUID) -> CourtResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )


@router.patch("/{public_id}", summary="TODO: update court pricing (manager)")
def update_court(public_id: UUID, _body: CourtUpdate) -> CourtResponse:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )


@router.delete(
    "/{public_id}",
    summary="TODO: deactivate court (manager)",
    status_code=status.HTTP_501_NOT_IMPLEMENTED,
)
def delete_court(public_id: UUID) -> None:
    raise HTTPException(
        status_code=status.HTTP_501_NOT_IMPLEMENTED, detail=f"{_TODO}: {public_id}"
    )
