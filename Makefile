.PHONY: help backend-install backend-dev backend-test backend-lint frontend-install frontend-dev frontend-build test

help:
	@echo "ma-famille monorepo"
	@echo "  make backend-install   install backend deps (pip)"
	@echo "  make backend-dev       run FastAPI dev server"
	@echo "  make backend-test      run backend pytest"
	@echo "  make backend-lint      run ruff check backend"
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

frontend-install:
	npm --prefix frontend install

frontend-dev:
	npm --prefix frontend run dev

frontend-build:
	npm --prefix frontend run build

test: backend-test frontend-build
