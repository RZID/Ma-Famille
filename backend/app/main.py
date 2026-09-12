from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import settings


def create_app() -> FastAPI:
    app = FastAPI(title=settings.app_name, version="0.1.0")

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", summary="Root info")
    def root() -> dict[str, str]:
        return {"service": settings.app_name, "env": settings.app_env}

    app.include_router(v1_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
