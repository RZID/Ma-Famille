FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app

EXPOSE 8000

# Migrate first (with retries — the DB lives on another VM and may lag
# behind), so the app never boots on a stale schema.
CMD ["sh", "-c", "for i in $(seq 1 15); do alembic upgrade head && break || sleep 2; done; exec uvicorn app.main:app --host 0.0.0.0 --port 8000"]
