# ma-famille backend (FastAPI)

## Dev

```bash
make backend-install   # creates .venv (uv if present) + installs deps
make backend-dev       # uvicorn :8000 via .venv
```

Endpoints:

- `GET /` — root info
- `GET /v1/health` — liveness probe (no DB)
- `GET /v1/health/db` — readiness probe (`SELECT 1`)
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
    core/security.py # X-Manager-Token gate
    db/              # Base, mixins, engine, SessionLocal, get_db, seed
    api/v1/          # health, venues, courts, slots, bookings, payments, manager
    models/          # Venue, Court, Slot, Booking, Payment
    schemas/         # Pydantic request/response models
    services/        # business logic (conflict guard, DOKU client, occupancy)
  tests/             # pytest (SQLite override, no live DB needed)
```

Manager writes need `X-Manager-Token` (see `MANAGER_TOKEN` in `.env.example`).
Payments go through the DOKU sandbox — see `docs/PAYMENTS.md`.
