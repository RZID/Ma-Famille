# ADR 0006: Vue 3 with Vite for the frontend

- Status: Accepted
- Date: 2026-09-12
- Deciders: frontend group

## Context

The frontend is a single-page app: venue/court browsing, an availability
calendar, booking flows, and a manager dashboard with an occupancy chart.
Students need fast feedback (`npm run dev`), a production build CI can
verify, and a component model that six groups can split by view without
colliding.

## Decision

Build the SPA with Vue 3 (`<script setup>` SFCs) bundled by Vite, with
Vue Router for the route table.

## Rationale

- Single-file components map one-to-one onto the domain split
  (`HomeView`, `HealthView`, later `VenueView`, `BookingView`), so groups
  own files instead of sharing them.
- Vite's instant dev server and `vite build` give the tightest feedback
  loop of the options, and the build is a one-line CI gate.
- Vue Router keeps routing declarative and separate from data fetching,
  which matches the `view → store → services/api.js` flow in
  `docs/ARCHITECTURE.md`.
- `<script setup>` removes boilerplate, leaving less surface for
  inconsistent patterns across groups.

## Consequences

- Positive: per-view ownership, fast HMR, build verified in CI.
- Negative: team commits to the Vue ecosystem; acceptable since the stack
  was fixed up front.
- No data fetching in router or templates; views stay thin.

## Alternatives considered

- React + Vite — rejected: larger API surface for the same SPA needs, and
  the stack decision (Vue 3) was already fixed for the course.
- Server-rendered framework (Nuxt/Next) — rejected: no SEO or SSR need;
  a static SPA talking to FastAPI is simpler to deploy and review.
