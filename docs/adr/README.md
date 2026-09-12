# Architecture Decision Records

Decisions are numbered sequentially (`NNNN-short-title.md`) and never edited
after acceptance — a new decision supersedes an old one via a new ADR.

Copy `0000-template.md` for new records. Keep each record to one concern and
write the *why*, not just the *what*.

## Index

| ADR | Title | Status |
|---|---|---|
| [0001](0001-monorepo-layout.md) | Monorepo layout for frontend, backend and docs | Accepted |
| [0002](0002-fastapi-backend.md) | FastAPI as the backend framework | Accepted |
| [0003](0003-postgresql-database.md) | PostgreSQL as the primary database | Accepted |
| [0004](0004-sqlalchemy-alembic.md) | SQLAlchemy 2.x with Alembic migrations | Accepted |
| [0005](0005-integer-pk-uuidv7-public-id.md) | Integer PK internally, UUIDv7 as public id | Accepted |
| [0006](0006-vue3-vite-frontend.md) | Vue 3 with Vite for the frontend | Accepted |
| [0007](0007-pinia-state.md) | Pinia for client state management | Accepted |
| [0008](0008-tailwind-css.md) | Tailwind CSS v4 for styling | Accepted |
| [0009](0009-compose-podman-support.md) | Compose file supporting Docker and Podman | Accepted |
| [0010](0010-github-actions-ci.md) | GitHub Actions CI with a PostgreSQL service | Accepted |
| [0011](0011-uv-project-venv.md) | uv with a project-local venv for Python | Accepted |
| [0012](0012-doku-sandbox-payments.md) | DOKU sandbox for third-party payments | Accepted |
| [0013](0013-single-domain-subpath.md) | Single domain with subpath routing | Accepted |
