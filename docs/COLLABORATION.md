# Collaboration — 6 groups x 6 members

36 students. To avoid merge conflicts, ownership is by **domain slice**, not by layer.

## Suggested ownership

| Group | Owns | Paths |
|---|---|---|
| group-1 | Venue | `backend/app/**/venue*`, `frontend/src/stores/venues*`, `frontend/src/views/*Venue*` |
| group-2 | Court | `backend/app/**/court*`, `frontend/src/stores/courts*`, `frontend/src/views/*Court*` |
| group-3 | Slot / Schedule | `backend/app/**/slot*`, availability service, calendar UI |
| group-4 | Booking + conflict guard | `backend/app/**/booking*`, booking flow UI |
| group-5 | Payment + roles | `backend/app/**/payment*`, Customer vs Manager gates |
| group-6 | Platform / QA | `docs/`, `.github/`, `Makefile`, e2e, seed data |

`app.js`, `api/v1/router.py`, `AppNav.vue` are **shared** — edit only via small PR with notice in chat.

See `.github/CODEOWNERS` for review routing.

## Workflow

1. Pick issue, create `feature/group-<n>-<topic>` from latest `develop`.
2. One domain per PR, keep diff < ~400 lines when possible.
3. Request review from CODEOWNER of touched domain + 1 other group for shared files.
4. Merge with **squash**, keep semantic title. No `Co-authored-by` trailers.
5. Sync `develop` daily (`git pull --rebase origin develop`).

## Conflict prevention

- Never two groups editing the same domain file in parallel without an issue comment.
- Backend contract first: update `docs/API_CONTRACT.md` before implementing endpoint.
- Frontend mocks via `services/api.js` until backend route lands — don't duplicate axios instances.
- Seed/contract changes announced to all groups.

## Roles in app

- **Customer:** browse venues/courts/slots, create booking, view payment status.
- **Venue Manager:** CRUD courts, set pricing/schedules, confirm/cancel bookings.

Enforcement is backend-side (future auth). UI gating alone is not sufficient.
