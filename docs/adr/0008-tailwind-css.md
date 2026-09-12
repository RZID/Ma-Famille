# ADR 0008: Tailwind CSS v4 for styling

- Status: Accepted
- Date: 2026-09-12
- Deciders: frontend group

## Context

Six groups styling views independently will drift — different spacings,
colors and hand-written CSS files that conflict on merge. The project needs
one styling idiom with no separate stylesheet architecture to maintain.

## Decision

Style exclusively with Tailwind CSS v4 utilities via the official Vite
plugin; `src/style.css` contains only `@import 'tailwindcss'`.

## Rationale

- Utilities in markup remove the whole category of "whose CSS file owns
  this class" conflicts between groups.
- The v4 Vite plugin compiles only used utilities, keeping the production
  CSS small without any purge configuration.
- No custom `<style>` blocks means reviews focus on structure, not on
  competing design tokens; spacing and color stay consistent by default.
- Version 4 over 3: no `tailwind.config.js` or PostCSS wiring needed, so
  setup is two lines (`vite.config.js` plugin + CSS import).

## Consequences

- Positive: zero stylesheet ownership disputes; build output verified to
  contain only used utilities.
- Negative: long class lists in templates; accepted as the standard
  Tailwind trade-off.
- New `<style>` blocks in components fail review unless justified.

## Alternatives considered

- Hand-written CSS / BEM — rejected: guarantees six dialects of CSS and
  merge conflicts in shared stylesheets.
- Component UI kit (e.g. Vuetify) — rejected: heavy, opinionated, and
  overkill for a booking CRUD UI; locks all groups into one vendor.
