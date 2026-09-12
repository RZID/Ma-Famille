# ADR 0007: Pinia for client state management

- Status: Accepted
- Date: 2026-09-12
- Deciders: frontend group

## Context

Server state (venues, slots, bookings, health) is fetched over HTTP and
shared between views and components. Without a convention, each group would
fetch in its own way — duplicated axios calls, stale copies of the same
slot list, and no single place to refresh after a `409` conflict.

## Decision

Manage all server state in Pinia stores, one file per domain
(`app.js` now; `venues.js`, `bookings.js` later). Components never call
axios directly.

## Rationale

- One store per domain mirrors the backend router split, so ownership
  transfers cleanly: the group owning `/bookings` owns `bookings.js`.
- Actions centralise the refresh-after-mutation logic (e.g. re-fetch slots
  after a booking `409`), which would otherwise scatter across views.
- Pinia's composition-style stores (`defineStore` with `ref`s) match the
  `<script setup>` style, keeping one idiom across the codebase.
- Devtools support makes shared-state bugs visible during group demos.

## Consequences

- Positive: single source of truth per domain; HTTP stays in
  `services/api.js`, state transitions in stores, rendering in views.
- Negative: trivial one-off fetches still go through a store action;
  accepted for consistency.
- New domains must add a store file; views importing axios directly fail
  review.

## Alternatives considered

- Vuex — rejected: verbose mutations/actions split for the same outcome;
  Pinia is the officially recommended successor.
- Fetch-in-component (no store) — rejected: duplicates requests and leaves
  no place for coordinated refresh after conflicts.
