from fastapi import APIRouter

router = APIRouter()


@router.get("/health", summary="Liveness probe")
def health() -> dict[str, str]:
    return {"status": "ok", "service": "ma-famille-api"}
