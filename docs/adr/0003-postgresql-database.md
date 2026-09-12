# ADR 0003: PostgreSQL as the primary database

- Status: Accepted
- Date: 2026-09-12
- Deciders: backend group

## Context

Slot booking needs concurrent-safe writes (two customers must never book the
same slot), time-range queries per court per day, and exclusion/unique
constraints the database itself enforces. Tests should run without a live
database, while CI and local dev use the real one.

## Decision

Use PostgreSQL 16 as the primary database; tests override the session with
in-memory SQLite and never touch Postgres.

## Rationale

- Conflict prevention belongs in the database, not just in application
  code: unique constraints and transactions make double-booking impossible
  even under race conditions, which is the core requirement of this system.
- Range-friendly types and indexes fit the availability calendar (slots per
  court per day) far better than a schemaless store.
- One `postgres:16-alpine` service in compose and CI gives every student
  the same database with one command (`make db-up`).

## Consequences

- Positive: data integrity is enforced at the lowest layer; local, CI and
  (later) production run the same engine.
- Negative: contributors need a container runtime for full local dev;
  mitigated by SQLite-backed unit tests that need no database at all.
- No raw SQL in routers or services; all access goes through the ORM
  session (`get_db`).

## Alternatives considered

- SQLite everywhere — rejected: no real concurrency story and weaker
  constraint support; unsafe for the booking-conflict requirement.
- MySQL/MariaDB — rejected: no decisive advantage for time-range workloads,
  and the team already standardised compose/CI images on Postgres.
- No database (in-memory store) — rejected: bookings must survive restarts.
