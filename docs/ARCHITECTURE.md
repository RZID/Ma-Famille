# Architecture

## Monorepo

```text
backend/   FastAPI, versioned under /api/v1
frontend/  Vue 3 SPA, talks to backend via axios
docs/      decisions + contracts
.github/   CI + PR template + ownership
```

No shared package yet. Contract between FE/BE is HTTP + `docs/API_CONTRACT.md`.
`VITE_API_URL` is the only runtime coupling.

## Backend (`backend/app`)

- `main.py` — app factory, CORS, includes `api/v1` router. No business logic here.
- `core/config.py` — `pydantic-settings`. All env via `Settings`, never `os.getenv` scattered.
- `api/v1/` — one router per domain file, composed in `api/v1/router.py`.
  Current: `health.py`. Next: `venues.py`, `courts.py`, `slots.py`, `bookings.py`, `payments.py`.
- `models/` — persistence models (planned).
- `schemas/` — request/response Pydantic models (planned).
- `services/` — availability + overlap prevention (planned). Routers stay thin.

Rules:

1. Routers validate + call service, services own transactions/rules.
2. Every new domain adds: model + schema + service + router + test.
3. Breaking API change → new version prefix, never silent break of `v1`.

## Frontend (`frontend/src`)

- `router/` — route table only. No fetching inside router.
- `services/api.js` — single axios instance. All HTTP here.
- `stores/` — one Pinia store per domain (`app.js` now, later `venues.js`, `bookings.js`…).
- `views/` — route-level pages (`HomeView`, `HealthView`).
- `components/` — reusable UI (`AppNav`, `HealthStatus`).

Flow: `view → store action → services/api.js → backend → store state → view`.

## Data (planned)

`Venue 1—* Court 1—* Slot 1—* Booking 1—1 Payment`.
Overlap guard lives in backend service + DB constraint, never only in UI.

## Environments

- Backend: `backend/.env` (see `.env.example`), loaded by `Settings`.
- Frontend: `frontend/.env*`, `VITE_API_URL` baked at `vite build`.
- Local dev: backend `:8000`, frontend `:5173`.
