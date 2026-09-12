from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import router as v1_router
from app.core.config import settings
from app.schemas.health import RootResponse

DESCRIPTION = """Sports Venue Booking API (futsal / badminton courts).

Domain routes (Venue, Court, Slot, Booking, Payment, Manager) exist as TODO
stubs returning 501 — Swagger-first, store logic lands per group next.
"""

OPENAPI_TAGS = [
    {"name": "health", "description": "Liveness and readiness probes."},
    {"name": "venues", "description": "TODO: venue CRUD (manager) + public list."},
    {"name": "courts", "description": "TODO: courts with weekday/weekend rates."},
    {"name": "slots", "description": "TODO: availability calendar per court per day."},
    {
        "name": "bookings",
        "description": "TODO: booking with conflict check, history, confirm/cancel.",
    },
    {"name": "payments", "description": "TODO: deposit/paid status (no gateway)."},
    {"name": "manager", "description": "TODO: incoming bookings + occupancy chart."},
]


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        description=DESCRIPTION,
        openapi_tags=OPENAPI_TAGS,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/", summary="Root info", response_model=RootResponse, tags=["health"])
    def root() -> RootResponse:
        return RootResponse(service=settings.app_name, env=settings.app_env)

    app.include_router(v1_router, prefix=settings.api_v1_prefix)

    return app


app = create_app()
