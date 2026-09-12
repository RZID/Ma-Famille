# ma-famille backend (FastAPI)

## Dev

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --app-dir . --port 8000
```

Endpoints:

- `GET /` — root info
- `GET /api/v1/health` — liveness probe (no DB)
- `GET /api/v1/health/db` — readiness probe (`SELECT 1`)
- `GET /docs` — Swagger UI (auto-generated OpenAPI)
- `GET /redoc` — ReDoc
- `GET /openapi.json` — raw OpenAPI spec

Run `make backend-dev`, then open http://localhost:8000/docs.

## Database

PostgreSQL + SQLAlchemy 2.x + Alembic. See `docs/DATABASE.md`.

```bash
make db-up
make db-upgrade
```

## Layout

```text
backend/
  alembic.ini
  alembic/          # env.py + versions/
  app/
    main.py          # app factory, CORS, router wiring
    core/config.py   # pydantic-settings (incl. DATABASE_URL)
    db/              # Base, engine, SessionLocal, get_db
    api/v1/          # versioned routers (health + future domains)
    models/          # ORM / domain models (planned: Venue, Court, Slot, Booking, Payment)
    schemas/         # Pydantic schemas (planned)
    services/        # business logic (planned: availability, conflict checks)
  tests/             # pytest
```

Domain modules are intentionally empty in the foundation iteration.
See `docs/API_CONTRACT.md` for the planned entities.
