FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS builder

# Stage 1
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1

WORKDIR /opt/app

COPY uv.lock .
COPY pyproject.toml .

RUN uv sync --frozen --no-install-project --no-dev --no-editable --no-cache

COPY package/app /opt/app/package/app
COPY package/tests /opt/app/package/tests
COPY assets /opt/app/package/assets
COPY package/alembic.ini /opt/app/package/alembic.ini
COPY package/__init__.py /opt/app/package/__init__.py
COPY README.md /opt/app/README.md

RUN uv sync --frozen --no-dev --no-editable --no-cache

COPY ./config/test.sh test.sh

ENV PATH="/opt/app/.venv/bin:$PATH"

# Use this entrypoint for running tests in docker
# This stage uses UV so you can install packages while running tests
# It can be split into two docker images, but i dont like that
CMD ["/opt/app/test.sh"]

# Final stage
FROM python:3.13 AS prod
ENV PYTHONUNBUFFERED=1

WORKDIR /opt/app

COPY --from=builder /opt/app/.venv .venv
COPY --from=builder /opt/app/package/app/alembic/ ./package/app/alembic/
COPY --from=builder /opt/app/package/alembic.ini alembic.ini

COPY ./config/run.sh run.sh
COPY ./config/migrate.sh migrate.sh

ENV PATH="/opt/app/.venv/bin:$PATH"

# This is not really needed, but it's a good practice to create a non-root user
# and change ownership of the working directory to that user.
# This is because the default user in the python:3.13 image is root.
RUN useradd -m user \
&& chown -R user . \
&& chmod -R 775 .
USER user

#Use this for running the normal app
CMD ["/opt/app/run.sh"]