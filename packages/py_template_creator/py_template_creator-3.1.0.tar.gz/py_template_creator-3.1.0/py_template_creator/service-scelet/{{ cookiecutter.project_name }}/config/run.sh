#!/usr/bin/env bash
set -e

# Default to "true" if RUN_MIGRATIONS is not set
RUN_MIGRATIONS=${RUN_MIGRATIONS:-true}

if [ "$RUN_MIGRATIONS" = "true" ]; then
    ./migrate.sh
fi
{{ cookiecutter.project_name }}
