# ADR 0011: uv with a project-local venv for Python

- Status: Accepted
- Date: 2026-09-12
- Deciders: platform group

## Context

Backend commands (`uvicorn`, `pytest`, `ruff`, `alembic`) failed with
`command not found` on machines without global Python tooling — some lab
images ship Python with no pip at all and no sudo to install it. Every
`make` target must work from a fresh checkout with one setup command.

## Decision

Standardise on a project-local `.venv` created by `make backend-install`
(using `uv` when present, `python3 -m venv` otherwise), and run every
backend `make` target through `$(VENV)/bin/python -m ...`.

## Rationale

- `uv` installs as a user-level binary with no sudo and provisions both
  the venv and the packages, which unblocks the exact machines that lack
  pip.
- A checked-in-path `.venv` (gitignored) means `make backend-dev` works
  without activating anything — no "did you source the venv?" failures
  across 36 students.
- `python -m <tool>` invocation removes reliance on console scripts being
  on `PATH`, the precise cause of the original `uvicorn: No such file`
  failure.
- Falling back to `python3 -m venv` + `pip` keeps the workflow usable
  where `uv` is not installed.

## Consequences

- Positive: fresh-machine setup is `make backend-install`; CI and local
  dev resolve tools identically.
- Negative: one more dot-directory per checkout (untracked, ~costless);
  students must not commit it.
- Python version upgrades happen by recreating `.venv`, never by touching
  system Python.

## Alternatives considered

- Global installs (`pip install`, system `uvicorn`) — rejected: requires
  sudo/pip that lab machines lack, and pollutes shared interpreters.
- Poetry/Pipenv — rejected: heavier lockfile workflow than 36 students
  need for a fixed `requirements-dev.txt`.
