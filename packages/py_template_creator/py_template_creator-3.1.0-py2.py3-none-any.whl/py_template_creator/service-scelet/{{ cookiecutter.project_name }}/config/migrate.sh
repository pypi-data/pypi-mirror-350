#!/usr/bin/env bash
echo "Running migrations..."
alembic -c alembic.ini ensure_version
alembic -c alembic.ini upgrade head