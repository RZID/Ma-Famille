#!/usr/bin/env bash
# Deploy the frontend over SSH to the edge static server. Used both locally and
# in CI.
#
# Usage:
#   DEPLOY_HOST=be-ssh.rzidinc.com DEPLOY_USER=deploy DEPLOY_APP_DIR=/home/deploy/ma-famille \
#     VITE_API_URL=https://college-api.rzidinc.com/ma-famille \
#     bash scripts/deploy-frontend.sh
# Env: DEPLOY_HOST, DEPLOY_USER, DEPLOY_APP_DIR, VITE_BASE_PATH, VITE_API_URL, SSH_OPTS
set -euo pipefail

DEPLOY_HOST="${DEPLOY_HOST:-be-ssh.rzidinc.com}"
DEPLOY_USER="${DEPLOY_USER:-deploy}"
DEPLOY_APP_DIR="${DEPLOY_APP_DIR:-/home/deploy/ma-famille}"
EDGE_DIR="${EDGE_DIR:-$DEPLOY_APP_DIR/../edge-dist/ma-famille}"
SSH_OPTS="${SSH_OPTS:-}"

export VITE_BASE_PATH="${VITE_BASE_PATH:-/ma-famille/}"
export VITE_API_URL="${VITE_API_URL:-https://college-api.rzidinc.com/ma-famille}"

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

# Every ssh/scp call goes through scripts/ssh-retry.sh — same reason as in
# deploy-backend.sh: the prod tunnel drops back-to-back SSH sessions.
SSH() { "$REPO_ROOT/scripts/ssh-retry.sh" ssh $SSH_OPTS "$DEPLOY_USER@$DEPLOY_HOST" "$@"; }
SCP() { "$REPO_ROOT/scripts/ssh-retry.sh" scp $SSH_OPTS "$@"; }

echo "==> build frontend (BASE=$VITE_BASE_PATH API=$VITE_API_URL)"
npm --prefix "$REPO_ROOT/frontend" ci
npm --prefix "$REPO_ROOT/frontend" run build

echo "==> deliver dist/ ke $DEPLOY_USER@$DEPLOY_HOST:$EDGE_DIR"
# shellcheck disable=SC2086
SSH "mkdir -p '$EDGE_DIR'"
# shellcheck disable=SC2086
SCP -r "$REPO_ROOT/frontend/dist/." "$DEPLOY_USER@$DEPLOY_HOST:$EDGE_DIR/"

echo "OK: frontend terkirim. Pastikan static server serve $EDGE_DIR di /ma-famille/"
