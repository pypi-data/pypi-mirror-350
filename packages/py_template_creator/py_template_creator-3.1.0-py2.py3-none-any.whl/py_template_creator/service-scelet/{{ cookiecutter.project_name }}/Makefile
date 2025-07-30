SHELL := /bin/bash
include ../.env
export

env:
	uv sync --all-extras

run:
	@echo "Running service..."
	uv run package/run.py

test:
	@echo "Running unit tests..."
	env POSTGRES_DB=test_db uv run coverage run -m pytest ${module} && \
	uv run coverage html && \
	uv run coverage report
	@echo
	@echo "Ruff errors in code ----------------"
	@echo
	@echo "--------------------------------------"
	uvx ruff check
	@echo "OK, no ruff errors in code"
	@echo "--------------------------------------"

lint:
	uvx ruff check

migrations:
	@echo "Generating migrations ..."
	uv run alembic -c ./package/alembic.ini revision --autogenerate -m "${message}"

migrate:
	@echo "Running migrations ..."
	uv run alembic -c ./package/alembic.ini upgrade head
	@echo "Migrations finished."

shell:
	uv run python package/shell.py

downgrade:
	@echo "Running downgrade ..."
	uv run alembic -c ./package/alembic.ini downgrade ${level}
	@echo "Migrations finished."

init_db:
	@echo "Initing database ..."
	uv run alembic -c ./package/alembic.ini ensure_version
	@echo "Migrations finished."

check_db:
	@echo "Checking migrations ..."
	uv run alembic -c ./package/alembic.ini check
	@echo "Migrations finished."
