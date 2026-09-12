from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.schemas.health import DbHealthResponse, HealthResponse

router = APIRouter()


@router.get("/health", summary="Liveness probe (no DB)", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse()


@router.get(
    "/health/db",
    summary="Readiness probe (SELECT 1)",
    response_model=DbHealthResponse,
    responses={503: {"description": "Database unreachable"}},
)
def health_db(db: Session = Depends(get_db)) -> DbHealthResponse:
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unreachable") from exc
    return DbHealthResponse()
