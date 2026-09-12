# Deployment

```text
browser ──HTTPS──▶ Cloudflare Pages (frontend, auto per push)
browser ──HTTPS──▶ cloudflared tunnel ──▶ 127.0.0.1:8000 (backend api, home server)
GitHub ──outbound only──▶ self-hosted runner (home server, no public IP needed)
```

## One-time server setup

1. Install Docker (or Podman) and `cloudflared`; the tunnel itself is
   unchanged, just add one ingress line:
   ```yaml
   ingress:
     - hostname: api.<your-domain>
       service: http://127.0.0.1:8000
   ```
2. Install the GitHub Actions runner
   (repo → Settings → Actions → Runners → New self-hosted runner),
   labels must include `ma-famille`, and register it as a systemd service
   so it survives reboots.
3. Clone the repo on the server once and create `backend/.env` there
   (DATABASE_URL is overridden by compose; add DOKU keys, and set
   `BACKEND_CORS_ORIGINS` to include the Pages URL, e.g.
   `https://ma-famille.pages.dev`).

## How a deploy flows

1. Push to `main` → `ci` runs (lint, migrate, pytest, vite build).
2. On CI success, `cd` fires automatically (`workflow_dispatch` forces one
   manually): the home-server runner rebuilds `compose.prod.yml`,
   the api container runs `alembic upgrade head` on boot, then the
   workflow curls the local health gate before finishing.

## Frontend (Cloudflare Pages)

Connect the repo in Pages with these settings — no workflow file needed:

| Setting | Value |
|---|---|
| Root directory | `frontend` |
| Build command | `npm run build` |
| Output directory | `dist` |
| Env (Production) | `VITE_API_URL=https://api.<your-domain>` |

Every PR gets a preview URL automatically. `public/_redirects` keeps
vue-router history mode working on refresh (`/health` must not 404).

## Rollback

Backend: `git revert <sha>` + push to `main` — CI/CD redeploys the
reverted tree like any other change. Frontend: Pages → Deployments →
Rollback to any previous deployment in one click.
