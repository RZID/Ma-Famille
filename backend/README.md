# ma-famille backend (FastAPI)

## Dev

```bash
pip install -r requirements-dev.txt
uvicorn app.main:app --reload --app-dir . --port 8000
```

Endpoints:

- `GET /` — root info
- `GET /api/v1/health` — liveness probe
- `GET /docs` — Swagger UI

## Layout

```text
backend/
  app/
    main.py          # app factory, CORS, router wiring
    core/config.py   # pydantic-settings
    api/v1/          # versioned routers (health + future domains)
    models/          # ORM / domain models (planned: Venue, Court, Slot, Booking, Payment)
    schemas/         # Pydantic schemas (planned)
    services/        # business logic (planned: availability, conflict checks)
  tests/             # pytest
```

Domain modules are intentionally empty in the foundation iteration.
See `docs/API_CONTRACT.md` for the planned entities.
