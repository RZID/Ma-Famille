#!/bin/sh
# The prod tunnel answers fine for a single SSH session, but it often refuses
# the very next one when a deploy opens sessions back to back — the client
# sees "websocket: bad handshake" and exits 255. The deploy ships several
# short sessions in a row, so every ssh/scp call goes through this wrapper:
# a failed connection is retried with a growing pause instead of failing the
# whole run.
#
# A retry must re-run on the SAME input, so stdin is slurped into a temp file
# first (when it is not a tty): a heredoc or `< file` is consumed to EOF by a
# failed attempt, and re-reading the exhausted stream would make the second
# attempt run an empty payload and exit 0 — a success that never happened.
# Every command behind this remains safe to run twice (mkdir, cat >, tar +
# compose), so a retry landing after a partial upload just overwrites it.
#
# Usage: sh scripts/ssh-retry.sh <ssh|scp> <ssh-or-scp-args...>
# Env:  SSH_RETRY_ATTEMPTS (default 5), SSH_RETRY_PAUSE (default 10)
set -eu

BIN="$1"
shift
ATTEMPTS="${SSH_RETRY_ATTEMPTS:-5}"
PAUSE_BASE="${SSH_RETRY_PAUSE:-10}"

TMP_STDIN=""
cleanup() { [ -n "$TMP_STDIN" ] && rm -f "$TMP_STDIN"; }
trap cleanup EXIT

if [ ! -t 0 ]; then
  TMP_STDIN=$(mktemp)
  cat > "$TMP_STDIN"
fi

n=0
while :; do
  n=$((n + 1))
  STATUS=0
  if [ -n "$TMP_STDIN" ]; then
    "$BIN" "$@" <"$TMP_STDIN" || STATUS=$?
  else
    "$BIN" "$@" </dev/null || STATUS=$?
  fi
  [ "$STATUS" -eq 0 ] && exit 0
  [ "$n" -ge "$ATTEMPTS" ] && exit "$STATUS"
  WAIT=$((PAUSE_BASE * n))
  echo "==> $BIN dropped (attempt $n/$ATTEMPTS, tunnel?) — retrying in ${WAIT}s" >&2
  sleep "$WAIT"
done
