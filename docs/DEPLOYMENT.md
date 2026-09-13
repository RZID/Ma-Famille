# Deployment

Final URLs (single domain, single origin):

```text
https://college.rzidinc.com/ma-famille            → frontend (nginx static)
https://college.rzidinc.com/ma-famille/api/v1/…   → backend (FastAPI, ROOT_PATH=/ma-famille)
https://college.rzidinc.com/ma-famille/docs       → Swagger UI
```

Traffic:

```text
browser ──HTTPS──▶ cloudflared tunnel (LXC) ──LAN──▶ 192.168.1.50:8080 (nginx web, backend VM)
                                                        ├─ /ma-famille/     → static SPA
                                                        └─ /ma-famille/api/ → proxy to api:8000
GitHub runner ──SSH over tunnel──▶ be-ssh.rzidinc.com ──LAN──▶ backend VM:22 (git pull + compose up)
Cloudflare Pages ── previews per PR only (cannot mount at a subpath)
```

No self-hosted runner anywhere: deploys run on GitHub-hosted runners and
reach the prod server through the tunnel, gated by a Zero Trust Access
service token (no public IP, no open SSH port).

Tunnel and app live on different hosts, so the ingress points at the
backend VM's LAN IP (give the VM a static IP or DHCP reservation, and open
`8080/tcp` for the LXC host, e.g. `ufw allow from <lxc-ip> to any port 8080`).

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
3. Create the deploy key + GitHub secrets + Access app from
   "One-time access setup" below (replaces any runner).
4. Clone the repo to `~/ma-famille` and create `backend/.env` from
   `backend/.env.prod.example` (fill `POSTGRES_PASSWORD`,
   `MANAGER_TOKEN`, DOKU keys).
5. Create the compose env file at repo root (`~/ma-famille/.env`) so
   image builds and `POSTGRES_*` interpolate — same passwords as step 4:
   ```bash
   POSTGRES_USER=mafamille
   POSTGRES_PASSWORD=change-me
   POSTGRES_DB=mafamille
   VITE_API_URL=https://college.rzidinc.com/ma-famille
   ```

## First deploy checklist

After the first green `cd` run, on the server:

```bash
docker compose -f docker-compose.yml -f compose.prod.yml exec api python -m app.db.seed
curl http://127.0.0.1:8080/ma-famille/api/v1/health/db
```

Then set the DOKU sandbox Notification URL to
`https://college.rzidinc.com/ma-famille/api/v1/payments/webhook/doku`
and run one real sandbox payment (see `docs/PAYMENTS.md`).

## How a deploy flows

1. Push to `main` (backend paths) → `ci` runs (lint, migrate, pytest).
2. The same push triggers `deploy`: GitHub installs cloudflared, opens SSH
   through the tunnel with the service token, then on the prod server runs
   `git pull --ff-only` + `podman compose up -d --build` (migrations run
   inside the api container on boot), then gates on the public `/ma-famille`
   health path before finishing. `workflow_dispatch` forces one manually.

## One-time access setup (instead of a runner)

On the backend VM, the `deploy` user needs GitHub read access (for
`git pull`) plus the SSH key GitHub will present:

```bash
# as user deploy on the VM
ssh-keygen -t ed25519 -f ~/.ssh/github -N ""   # read-only repo access
gh repo deploy-key add ~/.ssh/github.pub --repo RZID/Ma-Famille --allow-write=false
```

Then register in GitHub (repo → Settings → Secrets and variables → Actions):

| Secret / variable | Value |
|---|---|
| `SSH_PRIVATE_KEY` (secret) | key whose pubkey is in the VM's `~/.ssh/authorized_keys` |
| `CF_ACCESS_CLIENT_ID` (secret) | Zero Trust service token ID |
| `CF_ACCESS_CLIENT_SECRET` (secret) | Zero Trust service token secret |
| `DEPLOY_HOST` (secret) | `be-ssh.rzidinc.com` |
| `DEPLOY_USER` (variable, default `deploy`) | VM username |
| `DEPLOY_APP_DIR` (variable, default `/home/deploy/ma-famille`) | checkout path on the VM |

And in Cloudflare Zero Trust: protect `be-ssh.rzidinc.com` with an
Access app whose only rule allows that service token.

First checkout on the VM (once, so `git pull` has something to update):

```bash
git clone git@github.com:RZID/Ma-Famille.git /home/deploy/ma-famille
```

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
