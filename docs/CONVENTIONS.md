# Conventions

## Semantic commits

Format: `type(scope): subject` — imperative, lowercase, no trailing period, no attribution trailers.

Allowed `type`: `feat`, `fix`, `chore`, `docs`, `test`, `ci`, `refactor`, `perf`, `style`, `build`.

Allowed `scope`: `backend`, `frontend`, `docs`, `ci`, `repo`, or domain (`venue`, `court`, `slot`, `booking`, `payment`).

Examples:

```text
feat(backend): add venue CRUD router
feat(booking): prevent overlapping slot reservations
fix(frontend): handle expired session on api client
chore: initialize monorepo root with tooling and docs skeleton
test(backend): add pytest setup with health endpoint coverage
ci: add GitHub Actions for backend and frontend verification
docs: add architecture, conventions and 6x6 collaboration guide
```

Do NOT add `Co-authored-by`, `Generated-by`, or AI footers.

## Branching

- `main` — protected, always green (CI must pass).
- `develop` — integration branch.
- Feature: `feature/group-<1-6>-<short-topic>`, e.g. `feature/group-3-booking-conflict`.
- Fix: `fix/group-<n>-<short-topic>`.

Flow: `feature/... → PR to develop → review → merge → develop → PR to main`.

## Pull requests

- Small, one domain per PR.
- Fill `.github/PULL_REQUEST_TEMPLATE.md` (what/why, verify steps, group).
- 1 approval from another group for cross-domain changes.
- CI (`backend pytest+ruff`, `frontend build`) must pass.

## Code style

- Python: `ruff check backend`, line-length 100, `target py311`.
- JS/Vue: 2-space indent, `*.vue` SFC `<script setup>`, no logic in templates.
- Env: never commit `.env`. Update `*.env.example` in the same PR.
- Tests: backend change without `tests/test_*.py` needs justification in PR.
