from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.session import get_db

router = APIRouter()


@router.get("/health", summary="Liveness probe (no DB)")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ma-famille-api"}


@router.get("/health/db", summary="Readiness probe (SELECT 1)")
def health_db(db: Session = Depends(get_db)) -> dict[str, str]:
    try:
        db.execute(text("SELECT 1"))
    except Exception as exc:
        raise HTTPException(status_code=503, detail="database unreachable") from exc
    return {"status": "ok", "database": "reachable"}
