#!/bin/sh
# Container entrypoint: migrate first (the DB lives on another VM and may
# lag behind), then run the API. Kept as a file (not an inline CMD) because
# older compose implementations mangle quoted JSON-array commands.
set -e
for i in $(seq 1 15); do
  if alembic upgrade head; then
    break
  fi
  sleep 2
done
exec uvicorn app.main:app --host 0.0.0.0 --port 8000
