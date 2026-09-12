# Deployment

Final URLs (single domain, single origin):

```text
https://college.rzidinc.com/ma-famille            → frontend (nginx static)
https://college.rzidinc.com/ma-famille/api/v1/…   → backend (FastAPI, ROOT_PATH=/ma-famille)
https://college.rzidinc.com/ma-famille/docs       → Swagger UI
```

Traffic:

```text
browser ──HTTPS──▶ cloudflared tunnel ──▶ 127.0.0.1:8080 (nginx web)
                                              ├─ /ma-famille/     → static SPA
                                              └─ /ma-famille/api/ → proxy to api:8000
GitHub ──outbound only──▶ self-hosted runner (prod server, no public IP needed)
Cloudflare Pages ── previews per PR only (cannot mount at a subpath)
```

> Cloudflare Pages cannot serve at a subpath natively (custom domains are
> full hostnames), so the final domain is served from the prod server while
> Pages stays as the free preview environment. See ADR 0013.

## One-time server setup

On the server, run the checker first — it reports what is missing without
changing anything:

```bash
bash scripts/bootstrap-server.sh
```

1. Install Docker (or Podman) and `cloudflared` until the checker is happy.
2. Merge `tunnel/config.example.yml` into the existing tunnel config
   (specific paths before any catch-all), then restart cloudflared.
3. Install the GitHub Actions runner
   (repo → Settings → Actions → Runners → New self-hosted runner),
   labels must include `ma-famille`, and register it as a systemd service
   so it survives reboots.
4. Clone the repo to `~/ma-famille` and create `backend/.env` from
   `backend/.env.prod.example` (fill `POSTGRES_PASSWORD`,
   `MANAGER_TOKEN`, DOKU keys).

## How a deploy flows

1. Push to `main` → `ci` runs (lint, migrate, pytest, vite build).
2. On CI success, `cd` fires automatically (`workflow_dispatch` forces one
   manually): the prod-server runner rebuilds `compose.prod.yml`,
   the api container runs `alembic upgrade head` on boot, then the
   workflow curls the local health gate before finishing.

## Frontend

Two targets from the same `frontend/` source:

| Target | How | Env |
|---|---|---|
| Final domain (served by `web` on the server) | built into the nginx image during deploy | `VITE_API_URL=https://college.rzidinc.com/ma-famille`, `VITE_BASE_PATH=/ma-famille/` (compose defaults) |
| PR previews (Cloudflare Pages) | connect repo in Pages: root `frontend`, build `npm run build`, output `dist` | `VITE_API_URL=https://college.rzidinc.com/ma-famille`, no `VITE_BASE_PATH` (root) |

`public/_redirects` covers SPA fallback on Pages; on the final domain
nginx `try_files` does the same job, so `/ma-famille/health` never 404s
on refresh.

## Rollback

Backend: `git revert <sha>` + push to `main` — CI/CD redeploys the
reverted tree like any other change. Frontend: Pages → Deployments →
Rollback to any previous deployment in one click.
