# ma-famille

Monorepo for **Sports Venue Booking** (futsal / badminton courts, time-slot availability, conflict-free booking).

> Scope checkpoint: this iteration only sets up **folder structure + best practices**.
> Domain features (`Venue`, `Court`, `Schedule/Slot`, `Booking`, `Payment`) are intentionally NOT implemented yet.

## Stack

- **Frontend:** Vue 3 + Vite + Pinia + Vue Router + Axios (`frontend/`)
- **Backend:** FastAPI + Pydantic Settings + Pytest (`backend/`)
- **Tooling:** npm, pip, Ruff, GitHub Actions, Make

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

# 2. backend
pip install -r backend/requirements-dev.txt
make backend-dev
# -> http://localhost:8000/docs
# -> http://localhost:8000/api/v1/health

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

## Roles (planned)

- **Customer:** books a court.
- **Venue Manager:** manages courts, pricing, schedules.

## Collaboration

36 students in 6 groups of 6. Branching, ownership, and semantic commits are defined in:

- `docs/COLLABORATION.md`
- `docs/CONVENTIONS.md`
- `.github/CODEOWNERS`
