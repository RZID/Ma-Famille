# Database (PostgreSQL + SQLAlchemy + Alembic)

## URL

`DATABASE_URL` (default local):

```text
postgresql+psycopg://mafamille:mafamille@localhost:5432/mafamille
```

Override via `backend/.env` (see `backend/.env.example`). Tests override `get_db`
with in-memory SQLite, so `pytest` needs no live DB — but CI also runs
`alembic upgrade head` against real PostgreSQL 16.

## Local dev

```bash
cp backend/.env.example backend/.env
make db-up            # postgres:16 via docker (default)
make db-upgrade       # alembic upgrade head
make backend-dev      # uvicorn :8000
# GET /api/v1/health      liveness (no DB)
# GET /api/v1/health/db   readiness (SELECT 1)
```

## Podman (optional, Docker stays default)

Compose file uses only the portable compose spec — no engine-specific keys —
so the same `docker-compose.yml` runs under Podman.

```bash
make db-up CONTAINER_ENGINE=podman
make db-logs CONTAINER_ENGINE=podman
make db-down CONTAINER_ENGINE=podman

# or persist for the session:
export CONTAINER_ENGINE=podman
make db-up
```

Notes:

- Requires Podman 4.1+ with the `compose` subcommand (`podman compose version`).
  If only the standalone `podman-compose` script is installed, override instead:
  `make db-up COMPOSE="podman-compose"`.
- Named volume `pgdata` (not a bind mount), so no `:Z` SELinux relabel is needed.
- Rootless Podman can bind port 5432 (above 1024) without extra setup.
- CI (GitHub Actions) keeps using Docker; Podman is local-dev only.

## Migrations

Rules for 6 groups:

1. Model change → migration in same PR. Never edit DB by hand.
2. One logical change per revision, message like `add venue table`.
3. Autogenerate then review the diff — Alembic misses some constraints.

```bash
make db-migrate m="add venue table"
# review backend/alembic/versions/XXXX_*.py
make db-upgrade
make db-downgrade   # rollback one step to verify downgrade works
```

`alembic/env.py` loads `Base.metadata` via `app.models`, URL from `Settings`.
New model file must be imported in `app/models/__init__.py` or autogenerate
will silently skip it.

## Code layout

```text
backend/
  alembic.ini
  alembic/env.py            # URL from settings, metadata from Base
  alembic/versions/         # revisions only, no ad-hoc SQL
  app/db/base.py            # DeclarativeBase
  app/db/session.py         # engine, SessionLocal, get_db
  app/models/               # ORM models subclass Base
```

Routers depend on `get_db`, services receive a `Session` — never create
engines inside routers/services.
