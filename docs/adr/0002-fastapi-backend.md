# ADR 0002: FastAPI as the backend framework

- Status: Accepted
- Date: 2026-09-12
- Deciders: backend group

## Context

The backend must expose a versioned JSON API (`/api/v1/...`) with
auto-generated Swagger docs, request validation, and a test suite students
can run locally. The team knows Python; the framework choice is between the
Python options that fit a small JSON API.

## Decision

Build the API with FastAPI, Pydantic v2 models for schemas, and
`TestClient`-based pytest tests.

## Rationale

- FastAPI generates OpenAPI/Swagger from the code for free, which the
  project needs anyway for frontend-backend coordination across groups.
- Pydantic validation matches the contract-first workflow: schemas are
  written once and enforced at runtime.
- `TestClient` makes endpoint tests plain function calls, so students can
  add coverage per domain without learning a separate test harness.
- Async-ready without forcing async: health and CRUD endpoints stay simple
  sync functions today and can go async later without a rewrite.

## Consequences

- Positive: `/docs` is always in sync with the code; validation errors are
  uniform `422` responses.
- Negative: heavier dependency tree than a micro-framework; accepted
  because validation and docs would otherwise be hand-built.
- Routers must stay thin (`api/v1/` validates, `services/` decides) so the
  framework never leaks business rules into route handlers.

## Alternatives considered

- Django + DRF — rejected: too much machinery (admin, ORM opinions, project
  layout) for a versioned JSON API built by six parallel groups.
- Flask — rejected: no built-in validation or OpenAPI; every group would
  hand-roll the same helpers inconsistently.
