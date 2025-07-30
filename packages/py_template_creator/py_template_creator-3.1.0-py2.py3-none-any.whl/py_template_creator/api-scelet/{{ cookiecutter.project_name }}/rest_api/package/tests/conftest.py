import pytest
from contextlib import ExitStack
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory
from sqlalchemy.ext.asyncio import (
    create_async_engine,
    close_all_sessions,
)
from sqlalchemy.pool import NullPool
from sqlalchemy import text, inspect
from package.app.models import (
    DB_URL,
    Base,
    get_db_session,
    DatabaseSessionManager,
)
from package.app.main import app as actual_app
from package.app import settings
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def app(event_loop):
    with ExitStack():
        yield actual_app


@pytest.fixture
def client(event_loop, app):
    with TestClient(app) as c:
        yield c


@pytest.fixture(scope="session")
async def sessionmanager():
    yield DatabaseSessionManager(DB_URL, {"poolclass": NullPool})


@pytest.fixture(scope="session", autouse=True)
async def setup_database(sessionmanager):
    """Creates and applies migrations to a fresh test database."""
    ROOT_DB_URL = (
        f"postgresql+asyncpg://{settings.POSTGRES_USER}:"
        f"{settings.POSTGRES_PASSWORD}@{settings.POSTGRES_HOST}:"
        f"{settings.POSTGRES_PORT}/postgres"
    )

    my_engine = create_async_engine(
        ROOT_DB_URL,
        echo=True,
        isolation_level="AUTOCOMMIT",
        poolclass=NullPool,
    )  # connect to server
    async with my_engine.connect() as conn:
        await conn.execute(
            text("DROP DATABASE IF EXISTS test_db;")
        )  # create db
        await conn.execute(text("CREATE DATABASE test_db;"))  # create db
    async with sessionmanager.connect() as connection:
        await connection.run_sync(run_migrations)

    yield

    # Teardown
    await sessionmanager.close()


def run_migrations(connection):
    """Run Alembic migrations."""
    config = Config("package/alembic.ini")
    config.set_main_option("script_location", "package/app/alembic")
    config.set_main_option("sqlalchemy.url", DB_URL)

    script = ScriptDirectory.from_config(config)

    def upgrade(rev, context):
        return script._upgrade_revs("head", rev)

    context = MigrationContext.configure(
        connection, opts={"target_metadata": Base.metadata, "fn": upgrade}
    )

    with context.begin_transaction():
        with Operations.context(context):
            context.run_migrations()


@pytest.fixture(scope="function", autouse=True)
async def drop_tables():
    yield
    await close_all_sessions()

    my_engine = create_async_engine(
        DB_URL,
        echo=False,
        isolation_level="AUTOCOMMIT",
        poolclass=NullPool,
    )

    async with my_engine.connect() as conn:
        await conn.execute(text("SET session_replication_role = 'replica';"))

        table_names = await conn.run_sync(
            lambda sync_conn: inspect(sync_conn).get_table_names()
        )

        for table_name in table_names:
            await conn.execute(
                text(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE;')
            )

        await conn.execute(text("SET session_replication_role = 'origin';"))

        await conn.commit()

    await my_engine.dispose()


# Each test function is a clean slate
@pytest.fixture(scope="function", autouse=True)
async def transactional_session(sessionmanager):
    async with sessionmanager.session() as session:
        try:
            session.autoflush = True
            yield session
        finally:
            await session.rollback()


@pytest.fixture(scope="function")
async def session(transactional_session):
    yield transactional_session


@pytest.fixture(scope="function", autouse=True)
async def session_override(app, sessionmanager):
    async def get_db_session_override():
        async with sessionmanager.session() as session:
            try:
                session.autoflush = True
                yield session
            finally:
                await session.rollback()

    app.dependency_overrides[get_db_session] = get_db_session_override
