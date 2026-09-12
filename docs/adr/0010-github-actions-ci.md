# ADR 0010: GitHub Actions CI with a PostgreSQL service

- Status: Accepted
- Date: 2026-09-12
- Deciders: platform group

## Context

Six groups merging into `develop`/`main` need a gate that catches breakage
before review: backend lint plus migrations plus tests against the real
database, and a frontend production build. The gate must be automatic,
identical for every pull request, and free for a student project.

## Decision

Run GitHub Actions on `main`/`develop` pushes and all pull requests: a
backend job (ruff, `alembic upgrade head`, pytest) against a Postgres 16
service container, and a frontend job (`npm ci`, `vite build`).

## Rationale

- The code already lives on GitHub, so Actions needs no new accounts,
  runners or secrets for a student team.
- A Postgres *service* (not SQLite) in CI means migrations are exercised
  against the real engine on every PR — the exact step students skip
  locally.
- Splitting backend/frontend jobs keeps failures attributable: a UI-only
  PR never waits on database setup confusion, and vice versa.
- `main` and `develop` stay green by construction since merges require the
  gate.

## Consequences

- Positive: broken migrations and lint errors are caught before human
  review; `develop` is always demoable.
- Negative: CI minutes and occasional runner flakiness; mitigated by pip
  and npm caching.
- New backend dependencies must install cleanly from
  `requirements-dev.txt`; new frontend code must survive `vite build`.

## Alternatives considered

- No CI, local checks only — rejected: with 36 contributors, "works on my
  machine" is guaranteed without a shared gate.
- Self-hosted runner (Jenkins/Act) — rejected: maintenance burden no
  student group signed up for.
