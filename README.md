# ma-famille

Monorepo for **Sports Venue Booking** (futsal / badminton courts, time-slot availability, conflict-free booking).

Backend is wired end-to-end (venues → courts → slots → bookings → payments + manager dashboard); frontend views are the next track.

## Stack

- **Frontend:** Vue 3 + Vite + Pinia + Vue Router + Axios + Tailwind CSS (`frontend/`)
- **Backend:** FastAPI + SQLAlchemy + Alembic + PostgreSQL + Pytest (`backend/`)
- **Payments:** DOKU sandbox + signed webhook (`docs/PAYMENTS.md`)
- **Tooling:** uv, npm, Ruff, GitHub Actions, Make, Docker/Podman compose

## Layout

```text
ma-famille/
  backend/            # FastAPI app (app/*, tests/*)
  frontend/           # Vue 3 + Vite app (src/*)
  docs/               # architecture, conventions, collaboration, api-contract
  .github/workflows/  # CI
  Makefile            # shortcuts
  .env.example        # shared env template
```

See `docs/ARCHITECTURE.md` for module boundaries and `docs/COLLABORATION.md` for the 6 groups x 6 members workflow.

## Quickstart

Requirements: Python 3.11+, Node 20+, npm 10+.

```bash
# 1. env
cp .env.example .env
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env

# 2. backend (uv recommended: curl -LsSf https://astral.sh/uv/install.sh | sh)
make backend-install
make backend-dev
# -> http://localhost:8000/docs
# -> http://localhost:8000/v1/health

# 3. frontend (new terminal)
npm --prefix frontend install
npm --prefix frontend run dev
# -> http://localhost:5173
```

## Scripts

| Command | Purpose |
|---|---|
| `make backend-test` | `pytest backend/tests -v` |
| `make backend-lint` | `ruff check backend` |
| `make frontend-build` | `vite build` |
| `make test` | backend tests + frontend build |

## Roles

- **Customer:** books a court (open routes).
- **Venue Manager:** manages courts, pricing, schedules (`X-Manager-Token`).

## Collaboration

36 students in 6 groups of 6. Branching, ownership, and semantic commits are defined in:

- `docs/COLLABORATION.md`
- `docs/CONVENTIONS.md`
- `.github/CODEOWNERS`
