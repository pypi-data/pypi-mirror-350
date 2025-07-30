ARG PYTHON_VERSION=3.12-bookworm-slim
ARG REGISTRY=registry.git.bridgewaterlabs.com/wemind/wemind-backend

# Stage 1
FROM ${REGISTRY}/python:${PYTHON_VERSION}-uv AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy PYTHONUNBUFFERED=1

ARG APP_DIR
WORKDIR /opt/app

COPY ./${APP_DIR}/uv.lock .
COPY ./${APP_DIR}/pyproject.toml .
COPY ./shared /opt/shared

RUN uv sync --frozen --no-install-project --no-dev --no-editable --no-cache

COPY ./${APP_DIR}/package/app /opt/app/package/app
COPY ./${APP_DIR}/package/tests /opt/app/package/tests
COPY ./${APP_DIR}/package/__init__.py /opt/app/package/__init__.py
COPY ./${APP_DIR}/package/alembic.ini /opt/app/package/alembic.ini
COPY ./${APP_DIR}/package/run.py /opt/app/package/run.py
COPY ./${APP_DIR}/config /opt/app/config
COPY ./${APP_DIR}/README.md /opt/app/README.md

RUN uv sync --frozen --no-dev --no-editable --no-cache

COPY ./$APP_DIR/config/test.sh test.sh

ENV PATH="/opt/app/.venv/bin:$PATH"

CMD ["/opt/app/test.sh"]

# Final stage
FROM ${REGISTRY}/python:${PYTHON_VERSION} AS prod
ENV PYTHONUNBUFFERED=1
ARG APP_DIR

WORKDIR /opt/app

COPY --from=builder /opt/app/.venv .venv
COPY --from=builder /opt/app/package/app/alembic/ ./package/app/alembic/
COPY --from=builder /opt/app/package/alembic.ini alembic.ini

COPY ./$APP_DIR/config/run.sh run.sh
COPY ./$APP_DIR/config/migrate.sh migrate.sh

ENV PATH="/opt/app/.venv/bin:$PATH"

RUN useradd -m user \
&& chown -R user . \
&& chmod -R 775 .
USER user

CMD ["/opt/app/run.sh"]