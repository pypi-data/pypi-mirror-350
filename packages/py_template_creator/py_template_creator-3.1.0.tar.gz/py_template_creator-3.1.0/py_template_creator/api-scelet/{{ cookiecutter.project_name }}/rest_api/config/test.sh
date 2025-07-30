#!/bin/sh
set -e  # Configure shell so that if one command fails, it exits
export POSTGRES_DB=test_db
uv sync --frozen --all-extras --no-editable --no-cache
coverage erase
coverage run -m pytest
ruff check
coverage report
coverage html
coverage-badge

