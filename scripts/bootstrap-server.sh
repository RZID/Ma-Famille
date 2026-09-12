#!/usr/bin/env bash
# Prod-server bootstrap for ma-famille backend (run ON the server, once).
# Checks prerequisites, never deletes anything. Run: bash scripts/bootstrap-server.sh
set -u

ok() { echo "  [ok] $1"; }
warn() { echo "  [!!] $1"; }
have() { command -v "$1" >/dev/null 2>&1; }

echo "== 1. container engine =="
if have docker; then
  ok "docker $(docker --version | head -n1)"
elif have podman; then
  ok "podman $(podman --version)"
else
  warn "no docker/podman. Install docker: curl -fsSL https://get.docker.com | sh"
fi
if docker compose version >/dev/null 2>&1; then
  ok "docker compose plugin present"
elif have podman; then
  ok "use CONTAINER_ENGINE=podman (see Makefile)"
else
  warn "docker compose plugin missing"
fi

echo "== 2. cloudflared =="
if have cloudflared; then
  ok "cloudflared present — add ingress from tunnel/config.example.yml"
else
  warn "no cloudflared. Install: https://developers.cloudflare.com/cloudflare-one/connections/connect-networks/downloads/"
fi

echo "== 3. repo checkout =="
if [ -d "$HOME/ma-famille/.git" ]; then
  ok "$HOME/ma-famille already cloned"
else
  warn "clone first: git clone git@github.com:RZID/Ma-Famille.git $HOME/ma-famille"
fi

echo "== 4. backend env =="
if [ -f "$HOME/ma-famille/backend/.env" ]; then
  ok "backend/.env exists"
else
  warn "missing backend/.env — copy backend/.env.prod.example and fill secrets"
fi

echo "== 5. ports =="
for port in 8080 8000; do
  if (echo >/dev/tcp/127.0.0.1/$port) >/dev/null 2>&1; then
    warn "127.0.0.1:$port already in use"
  else
    ok "127.0.0.1:$port free"
  fi
done

echo "== 6. runner =="
warn "install manually: repo Settings → Actions → Runners → New self-hosted runner (label: ma-famille), then ./svc.sh install + start"
echo "done."
