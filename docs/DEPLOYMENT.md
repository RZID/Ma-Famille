# Deployment

Final URLs:

```text
https://college-api.rzidinc.com/ma-famille/v1/…   → backend (FastAPI, ROOT_PATH=/ma-famille)
https://college-api.rzidinc.com/ma-famille/docs       → Swagger UI
(frontend lives on Cloudflare Pages under its own hostname)
```

Traffic:

```text
browser ──HTTPS──▶ cloudflared tunnel (LXC) ──LAN──▶ 10.10.0.30:8000 (api, backend VM)
GitHub runner ──SSH over tunnel──▶ be-ssh.rzidinc.com ──LAN──▶ backend VM:22 (tarball + compose up)
Cloudflare Pages ── frontend (own Pages project + hostname)
```

No self-hosted runner anywhere: deploys run on GitHub-hosted runners and
reach the prod server through the tunnel, gated by a Zero Trust Access
service token (no public IP, no open SSH port).

Tunnel and app live on different hosts, so the ingress points at the
backend VM's LAN IP (give the VM a static IP or DHCP reservation).

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
2. Add the two tunnel hostnames in the dashboard
   (Zero Trust → Networks → Tunnels → Public Hostnames) —
   see `tunnel/config.example.yml` for the exact table.
   The tunnel runs in token mode, so no local config file is involved.
3. Create the deploy key + GitHub secrets + Access app from
   "One-time access setup" below (replaces any runner).
4. Create `backend/.env` on the server from
   `backend/.env.prod.example` (fill `DATABASE_URL`, `POSTGRES_PASSWORD`,
   `MANAGER_TOKEN`, DOKU keys). The tarball deploy wipes the checkout each
   run but never touches `backend/.env` or root `.env` — create them once.
5. Create the compose env file at repo root (`~/ma-famille/.env`) so
   `POSTGRES_*` interpolate:
   ```bash
   POSTGRES_USER=mafamille
   POSTGRES_PASSWORD=change-me
   POSTGRES_DB=mafamille
   ```

## First deploy checklist

After the first green `deploy` run, on the server:

```bash
podman compose -f docker-compose.yml -f compose.prod.yml exec api python -m app.db.seed
curl http://127.0.0.1:8000/ma-famille/v1/health/db
```

Then set the DOKU sandbox Notification URL to
`https://college-api.rzidinc.com/ma-famille/v1/payments/webhook/doku`
and run one real sandbox payment (see `docs/PAYMENTS.md`).

## How a deploy flows

1. Push to `main` (backend paths) → `ci` runs (lint, migrate, pytest).
2. The same push triggers `deploy`: GitHub installs cloudflared, opens SSH
   through the tunnel with the service token, then on the prod server
   extracts the tarball + `podman compose up -d --build` (migrations run
   inside the api container on boot), then gates on the `/ma-famille`
   health path before finishing. `workflow_dispatch` forces one manually.

## One-time access setup (instead of a runner)

The deploy ships a tarball, so the VM needs no GitHub access at all.
On the backend VM, as user `deploy`, authorize GitHub's key once:

```bash
# paste the SSH_PRIVATE_KEY's public counterpart here
echo '<deploy-pubkey>' >> ~/.ssh/authorized_keys
chmod 600 ~/.ssh/authorized_keys
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

## Frontend

Production FE is served by the edge static server on the VM
(`~/edge-dist/ma-famille`, delivered by the `deploy` workflow on every
push). Cloudflare Pages (`ma-famille` project) is previews only:
`web` workflow builds root-base and deploys on every `frontend/**` push.

Needs two secrets: `CLOUDFLARE_API_TOKEN` (Pages:Edit) and
`CLOUDFLARE_ACCOUNT_ID`.

## Rollback

Backend: `git revert <sha>` + push to `main` — CI/CD redeploys the
reverted tree like any other change. Frontend: Pages → Deployments →
Rollback to any previous deployment in one click.
