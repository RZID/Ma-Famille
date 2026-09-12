# ADR 0005: Integer PK internally, UUIDv7 as public id

- Status: Accepted
- Date: 2026-09-12
- Deciders: backend group

## Context

Every row needs an identifier for two different audiences: the database
itself (foreign keys, joins, migrations) and API clients (URLs, payloads).
Exposing sequential integers leaks business information (row counts, growth
rate) and makes client-side references guessable; exposing only random ids
hurts join performance and readability in the database.

## Decision

Each table gets both: an autoincrement `BigInteger id` used only for primary
keys, foreign keys and joins, and a unique indexed `public_id` (UUIDv7) that
is the sole identifier clients ever see. Mixins live in `app/db/base.py`;
generation lives in `app/core/ids.py`.

## Rationale

- Integer PKs keep joins narrow, FK definitions simple, and migrations
  predictable — the database stays fast without client concerns leaking in.
- UUIDv7 (time-ordered, RFC 9562) beats random v4 GUIDs as a public id:
  roughly sortable by creation time and friendlier to B-tree indexes, while
  its 74 random bits stay unguessable in URLs.
- The generator is stdlib-only, so the `requires-python >= 3.11` floor
  holds even where `uuid.uuid7` does not exist yet.
- A shared mixin triple (`PKMixin`, `PublicIdMixin`, `TimestampMixin`)
  makes the rule automatic: a model without a public id fails review.

## Consequences

- Positive: clients get opaque, non-enumerable ids; the schema keeps cheap
  integer joins; creation order is approximately recoverable from ids.
- Negative: slightly wider rows and two indexes per table; negligible at
  this scale.
- Serializers must expose `public_id` and never `id`; tests assert the
  contract.

## Alternatives considered

- Integer ids exposed publicly — rejected: enumerable, leaks row counts.
- Random v4 GUIDs as sole id — rejected: scatters B-tree inserts and gives
  up time-ordering for no security gain over v7.
- v7 as the primary key — rejected: wider PKs bloat every FK and index for
  no measurable benefit here.
