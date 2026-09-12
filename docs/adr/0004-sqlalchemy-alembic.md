# ADR 0004: SQLAlchemy 2.x with Alembic migrations

- Status: Accepted
- Date: 2026-09-12
- Deciders: backend group

## Context

Six groups will evolve the same schema (venues, courts, slots, bookings,
payments) in parallel. Schema changes must be reviewable, reversible, and
applicable identically in local dev and CI — never hand-edited in the
database.

## Decision

Use SQLAlchemy 2.x (`Mapped`/`mapped_column` style) as the ORM and Alembic
with autogenerate for versioned migrations, one logical change per revision.

## Rationale

- SQLAlchemy 2.x typing (`Mapped[int]`) makes model definitions explicit and
  lets reviewers see column types at a glance in pull requests.
- Alembic revisions are plain files under `alembic/versions/`, so a schema
  change is reviewed like code and rolls back with `downgrade`.
- Autogenerate from `Base.metadata` catches the common case (new tables and
  columns); the mandatory human review of the generated diff catches what it
  misses (constraints, data migrations).
- `alembic/env.py` reads the URL from `Settings` and metadata from
  `app.models`, so there is exactly one source of truth for connection and
  schema.

## Consequences

- Positive: `make db-migrate m="..."` / `make db-upgrade` is the whole
  workflow; CI runs `alembic upgrade head` before tests.
- Negative: autogenerate diffs must be read carefully; every PR touching
  models must include its migration.
- New model modules must be imported in `app/models/__init__.py`, otherwise
  autogenerate silently skips them.

## Alternatives considered

- Raw SQL migration files — rejected: no model-to-schema link, drift
  between code and database is invisible until runtime.
- Django ORM — rejected: follows from ADR 0002; would also force Django's
  project layout on all groups.
- Schemaless document store — rejected: the domain is relational (venue →
  court → slot → booking → payment) and needs joinable constraints.
