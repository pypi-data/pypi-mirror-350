import pytest
import contextlib
from alembic.config import Config
from alembic.migration import MigrationContext
from alembic.operations import Operations
from alembic.script import ScriptDirectory

from sqlalchemy.pool import NullPool
from sqlalchemy import text, create_engine, inspect
from sqlalchemy.orm import close_all_sessions
from package.app import settings
from package.app.models import Base, Session
from package.app.models.base import DB_URL


def truncate_all_tables(engine):
    inspector = inspect(engine)
    with engine.connect() as conn:
        conn.execute(text("SET session_replication_role = 'replica';"))
        for table_name in inspector.get_table_names():
            conn.execute(
                text(f'TRUNCATE TABLE "{table_name}" RESTART IDENTITY CASCADE;')
            )
        conn.execute(text("SET session_replication_role = 'origin';"))


def run_migrations(connection):
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


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # Run alembic migrations on test DB
    ROOT_DB_URL = "postgresql+psycopg://{}:{}@{}:{}/{}".format(
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
        settings.POSTGRES_PORT,
        "postgres",
    )
    my_engine = create_engine(
        ROOT_DB_URL,
        echo=False,
        isolation_level="AUTOCOMMIT",
        poolclass=NullPool,
    )  # connect to server
    with my_engine.connect() as conn:
        conn.execute(text("DROP DATABASE IF EXISTS test_db;"))
        conn.execute(text("CREATE DATABASE test_db;"))
    test_engine = create_engine(
        DB_URL,
        echo=False,
        isolation_level="AUTOCOMMIT",
        poolclass=NullPool,
    )
    with contextlib.closing(test_engine.connect()) as conn:
        run_migrations(connection=conn)


@pytest.fixture(scope="function", autouse=True)
def drop_tables():
    yield
    close_all_sessions()
    TEST_DB_URL = "postgresql+psycopg://{}:{}@{}:{}/{}".format(
        settings.POSTGRES_USER,
        settings.POSTGRES_PASSWORD,
        settings.POSTGRES_HOST,
        settings.POSTGRES_PORT,
        "test_db",
    )
    my_engine = create_engine(
        TEST_DB_URL,
        echo=False,
        isolation_level="AUTOCOMMIT",
        poolclass=NullPool,
    )  # connect to server
    truncate_all_tables(my_engine)


@pytest.fixture(scope="function")
def db():
    yield Session()
    Session.close()
