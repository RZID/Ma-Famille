# ADR 0013: Single domain with subpath routing

- Status: Accepted
- Date: 2026-09-13
- Deciders: platform group

## Context

The final URLs must live on one domain: the SPA at
`college.rzidinc.com/ma-famille` and the API at
`college.rzidinc.com/ma-famille/api/<version>/...`. The frontend source is
shared between the final domain and Cloudflare Pages previews, and the
backend runs on a home server behind a Cloudflare Tunnel.

## Decision

Serve both from one nginx origin on the home server: static SPA at
`/ma-famille/` (with SPA fallback) and a prefix-preserving proxy at
`/ma-famille/api/` to FastAPI with `ROOT_PATH=/ma-famille`. Cloudflare
Pages stays as the preview environment only.

## Rationale

- Pages custom domains are full hostnames; a project cannot mount at a
  subpath natively, so Pages alone cannot produce the required URLs —
  verified against Cloudflare docs before deciding.
- One origin removes CORS from the final domain entirely (same scheme,
  host and port for app and API); `BACKEND_CORS_ORIGINS` only matters for
  previews and local dev.
- Keeping the `/ma-famille` prefix end-to-end (Vite `base`, router
  `BASE_URL`, FastAPI `root_path`) means `/docs` and asset URLs are
  correct with no rewrites — rewrites are where subpath hosting usually
  breaks.
- Pages previews remain free per-PR environments, so nothing already built
  is thrown away.

## Consequences

- Positive: one tunnel ingress, no CORS in production, refresh works on
  every route via nginx `try_files`.
- Negative: the final frontend deploys with the backend (no independent
  Pages production deploy); acceptable since both move together per push
  to `main`.
- `VITE_BASE_PATH` must stay `/ma-famille/` for the server image and unset
  for Pages; mixing them up produces blank pages with 404 assets.

## Alternatives considered

- Worker in front routing to Pages + tunnel — rejected: an extra runtime
  (wrangler, worker deploys, two failure domains) for 36 students to
  operate, to save nothing the single origin cannot do.
- `api.` subdomain for the backend — rejected: contradicts the required
  URL layout.
- Prefix-stripping proxy without `root_path` — rejected: breaks `/docs`
  and `openapi.json` URLs, which are generated from the app root.
