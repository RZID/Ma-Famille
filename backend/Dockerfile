FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /srv/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY alembic.ini ./
COPY alembic ./alembic
COPY app ./app
COPY entrypoint.sh ./

EXPOSE 8000

# Migrate first (with retries — the DB lives on another VM and may lag
# behind), so the app never boots on a stale schema.
CMD ["sh", "entrypoint.sh"]
