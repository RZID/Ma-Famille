#!/usr/bin/env bash
# Deploy backend via SSH — dipakai lokal DAN GitHub Actions (deploy.yml).
# Di CI, DEPLOY_HOST=prod (ssh alias via cloudflared) + TUNNEL_* env.
#
# Usage:
#   DEPLOY_HOST=be-ssh.rzidinc.com DEPLOY_USER=deploy DEPLOY_APP_DIR=/home/deploy/ma-famille \
#     bash scripts/deploy-backend.sh
# Env yang didukung: DEPLOY_HOST, DEPLOY_USER, DEPLOY_APP_DIR, SSH_OPTS
set -euo pipefail

DEPLOY_HOST="${DEPLOY_HOST:-be-ssh.rzidinc.com}"
DEPLOY_USER="${DEPLOY_USER:-deploy}"
DEPLOY_APP_DIR="${DEPLOY_APP_DIR:-/home/deploy/ma-famille}"
SSH_OPTS="${SSH_OPTS:-}"

SSH="ssh $SSH_OPTS $DEPLOY_USER@$DEPLOY_HOST"
SCP="scp $SSH_OPTS"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARBALL="/tmp/mafamille-app.tgz"

echo "==> pack HEAD -> $TARBALL"
git -C "$REPO_ROOT" archive --format=tar.gz -o "$TARBALL" HEAD

echo "==> deliver ke $DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_APP_DIR"
# shellcheck disable=SC2086
$SSH "mkdir -p '$DEPLOY_APP_DIR'"
# shellcheck disable=SC2086
$SCP "$TARBALL" "$DEPLOY_USER@$DEPLOY_HOST:$DEPLOY_APP_DIR/app.tgz"

echo "==> deploy di server (podman compose up -d --build)"
# shellcheck disable=SC2086
$SSH "DEPLOY_APP_DIR='$DEPLOY_APP_DIR' sh -s" <<'EOF'
set -e
cd "$DEPLOY_APP_DIR"
tar xzf app.tgz && rm app.tgz
if podman compose version >/dev/null 2>&1; then COMPOSE="podman compose"; else COMPOSE="podman-compose"; fi
# Down dulu: compose lama kadang keep container stale.
$COMPOSE -f docker-compose.yml -f compose.prod.yml down 2>/dev/null || true
$COMPOSE -f docker-compose.yml -f compose.prod.yml up -d --build
if command -v curl >/dev/null; then FETCH="curl -fsS"; else FETCH="wget -q -O /dev/null"; fi
i=0
while [ $i -lt 30 ]; do
  if $FETCH http://127.0.0.1:8000/ma-famille/v1/health >/dev/null; then
    echo "prod api healthy"
    exit 0
  fi
  sleep 2
  i=$((i + 1))
done
echo "prod stack never became healthy" >&2
$COMPOSE -f docker-compose.yml -f compose.prod.yml logs --tail=50 api
exit 1
EOF

echo "==> prune old images"
# shellcheck disable=SC2086
$SSH 'podman image prune -f' || true

echo "OK: backend live. Cek: curl http://127.0.0.1:8000/ma-famille/v1/health (di server)"
