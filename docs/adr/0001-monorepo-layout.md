# ADR 0001: Monorepo layout for frontend, backend and docs

- Status: Accepted
- Date: 2026-09-12
- Deciders: all groups

## Context

Thirty-six students in six groups build one booking system with a Vue
frontend, a FastAPI backend, shared docs and CI. The team needs atomic
cross-layer changes (e.g. a booking endpoint plus its UI), one visible
history, and a single CI gate — while six groups must avoid stepping on
each other's files.

## Decision

Keep everything in one repository under `backend/`, `frontend/`, `docs/`
and `.github/`, with the HTTP contract (`docs/API_CONTRACT.md`) as the only
coupling point between frontend and backend.

## Rationale

- A booking feature spans API, UI and contract docs; a monorepo merges those
  as one reviewable pull request instead of three coordinated merges.
- One `git log`, one branching model and one CI workflow scale better for
  students than synchronising versions across repositories.
- Domain-sliced ownership (`docs/COLLABORATION.md`, `CODEOWNERS`) gives each
  group a clear slice, which removes the main monorepo risk — merge
  conflicts — without extra tooling.

## Consequences

- Positive: single checkout, single `make help`, contract changes are
  visible next to the code that implements them.
- Negative: the clone is larger and CI runs both stacks on every change;
  mitigated by per-job caching and small pull requests.
- The team must respect domain ownership and keep pull requests to one
  domain each.

## Alternatives considered

- Polyrepo (one repo per stack) — rejected: cross-layer features would need
  coordinated merges across repos, too costly for student teams.
- Monorepo with a shared code package — rejected: premature coupling; HTTP
  plus a written contract is enough at this stage.
