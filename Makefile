.PHONY: help backend-install backend-dev backend-test backend-lint db-up db-down db-logs db-migrate db-upgrade db-downgrade frontend-install frontend-dev frontend-build test

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
	@echo "ma-famille monorepo (engine: $(CONTAINER_ENGINE))"
	@echo "  make backend-install   install backend deps (pip)"
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

backend-install:
	pip install -r backend/requirements-dev.txt

backend-dev:
	uvicorn app.main:app --reload --app-dir backend --port 8000

backend-test:
	pytest backend/tests -v

backend-lint:
	ruff check backend

db-up:
	$(COMPOSE) up -d db

db-down:
	$(COMPOSE) down

db-logs:
	$(COMPOSE) logs -f db

db-migrate:
	cd backend && alembic revision --autogenerate -m "$(m)"

db-upgrade:
	cd backend && alembic upgrade head

db-downgrade:
	cd backend && alembic downgrade -1

frontend-install:
	npm --prefix frontend install

frontend-dev:
	npm --prefix frontend run dev

frontend-build:
	npm --prefix frontend run build

test: backend-test frontend-build
