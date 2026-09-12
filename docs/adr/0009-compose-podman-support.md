# ADR 0009: Compose file supporting Docker and Podman

- Status: Accepted
- Date: 2026-09-12
- Deciders: platform group

## Context

Local development needs PostgreSQL with one command, but students work on
mixed machines: some have Docker, others (notably Fedora/RHEL labs) only
have rootless Podman. Hardcoding `docker compose` locks out the second
group; maintaining two compose files guarantees they drift apart.

## Decision

Keep a single portable `docker-compose.yml` (no engine-specific keys) and
select the engine in the Makefile via `CONTAINER_ENGINE` (`docker` by
default, `podman` on request).

## Rationale

- The compose spec subset used (service, ports, named volume, healthcheck)
  runs identically on both engines, so one file serves everyone.
- Docker stays the default because CI runners and most laptops already
  have it; Podman is opt-in per command or per session, never a flag day.
- A named volume (not a bind mount) avoids Podman's SELinux `:Z` relabel
  dance entirely.
- Port 5432 is above 1024, so rootless Podman binds it with no extra
  configuration.

## Consequences

- Positive: `make db-up` vs `make db-up CONTAINER_ENGINE=podman` is the
  whole difference; no duplicated definitions.
- Negative: exotic compose features are off-limits; acceptable since the
  file only defines a database.
- Podman users need 4.1+ with the `compose` subcommand (documented
  fallback: `COMPOSE="podman-compose"`).

## Alternatives considered

- Docker only — rejected: excludes lab machines where only Podman exists.
- Two compose files — rejected: doubled maintenance for zero functional
  difference.
- Postgres without containers (native install) — rejected: version drift
  across 36 machines.
