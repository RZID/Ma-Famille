.PHONY: help backend-venv backend-install backend-dev backend-test backend-lint db-up db-down db-logs db-migrate db-upgrade db-downgrade frontend-install frontend-dev frontend-build test

# Python env: all backend targets run inside .venv (no global pip needed).
# `make backend-install` creates it (via uv if present) and installs deps.
VENV ?= .venv
PY := $(CURDIR)/$(VENV)/bin/python

# Container engine: docker (default) or podman.
# Usage: make db-up                    # docker
#        make db-up CONTAINER_ENGINE=podman
#        export CONTAINER_ENGINE=podman  # persist for session
CONTAINER_ENGINE ?= docker
ifeq ($(CONTAINER_ENGINE),podman)
COMPOSE ?= podman compose
else
COMPOSE ?= docker compose
endif

help:
	@echo "ma-famille monorepo (engine: $(CONTAINER_ENGINE), venv: $(VENV))"
	@echo "  make backend-venv      create project venv (.venv)"
	@echo "  make backend-install   install backend deps into venv"
	@echo "  make backend-dev       run FastAPI dev server"
	@echo "  make backend-test      run backend pytest"
	@echo "  make backend-lint      run ruff check backend"
	@echo "  make db-up             start local PostgreSQL ($(COMPOSE))"
	@echo "  make db-down           stop local PostgreSQL"
	@echo "  make db-logs           follow db logs"
	@echo "  make db-migrate m=\"msg\"  create Alembic revision (autogenerate)"
	@echo "  make db-upgrade        apply migrations (alembic upgrade head)"
	@echo "  make db-downgrade      rollback one migration"
	@echo "  make frontend-install  install frontend deps (npm)"
	@echo "  make frontend-dev      run Vite dev server"
	@echo "  make frontend-build    build frontend"
	@echo "  make test              run all tests"

backend-venv:
	@test -x $(PY) || (command -v uv >/dev/null && uv venv $(VENV) || python3 -m venv $(VENV))

backend-install: backend-venv
	@if command -v uv >/dev/null; then uv pip install --python $(PY) -r backend/requirements-dev.txt; else $(PY) -m pip install -r backend/requirements-dev.txt; fi

backend-dev:
	$(PY) -m uvicorn app.main:app --reload --app-dir backend --port 8000

backend-test:
	$(PY) -m pytest backend/tests -v

backend-lint:
	$(PY) -m ruff check backend

db-up:
	$(COMPOSE) up -d db

db-down:
	$(COMPOSE) down

db-logs:
	$(COMPOSE) logs -f db

db-migrate:
	cd backend && $(PY) -m alembic revision --autogenerate -m "$(m)"

db-upgrade:
	cd backend && $(PY) -m alembic upgrade head

db-downgrade:
	cd backend && $(PY) -m alembic downgrade -1

frontend-install:
	npm --prefix frontend install

frontend-dev:
	npm --prefix frontend run dev

frontend-build:
	npm --prefix frontend run build

test: backend-test frontend-build
