import logging
import contextlib
from package.app import settings
from typing import Any, AsyncIterator

from sqlalchemy.ext.asyncio import (
    AsyncConnection,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)

from sqlalchemy.schema import MetaData
from sqlalchemy.orm import (
    DeclarativeBase,
    MappedAsDataclass,
)


class Base(MappedAsDataclass, DeclarativeBase):
    metadata = MetaData(
        naming_convention={
            "ix": "ix_%(column_0_label)s",
            "uq": "uq_%(table_name)s_%(column_0_name)s",
            "ck": "ck_%(table_name)s_%(constraint_name)s",
            "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
            "pk": "pk_%(table_name)s",
        }
    )

    """subclasses will be converted to dataclasses"""


logger = logging.getLogger(__name__)

DB_URL = "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
    settings.POSTGRES_USER,
    settings.POSTGRES_PASSWORD,
    settings.POSTGRES_HOST,
    settings.POSTGRES_PORT,
    settings.POSTGRES_DB,
)
logger.info(f"Connecting with conn string {DB_URL}")


class DatabaseSessionManager:
    def __init__(self, host: str = DB_URL, engine_kwargs: dict[str, Any] = {}):
        self._engine = create_async_engine(
            host,
            **engine_kwargs,
        )
        self._sessionmaker = async_sessionmaker(
            autocommit=False,
            expire_on_commit=False,
            autoflush=True,
            bind=self._engine,
        )

    async def close(self):
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")
        await self._engine.dispose()

        self._engine = None
        self._sessionmaker = None

    @contextlib.asynccontextmanager
    async def connect(self) -> AsyncIterator[AsyncConnection]:
        if self._engine is None:
            raise Exception("DatabaseSessionManager is not initialized")

        async with self._engine.begin() as connection:
            try:
                yield connection
            except Exception:
                await connection.rollback()
                raise

    @contextlib.asynccontextmanager
    async def session(self) -> AsyncIterator[AsyncSession]:
        if self._sessionmaker is None:
            raise Exception("DatabaseSessionManager is not initialized")

        session = self._sessionmaker()
        try:
            yield session
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


sessionmanager = DatabaseSessionManager(
    DB_URL,
    {
        "pool_pre_ping": True,
        "pool_size": settings.POOL_SIZE,
        "pool_recycle": 3600,
        "echo": False,
    },
)


async def get_db_session() -> AsyncSession:
    async with sessionmanager.session() as session:
        yield session


async def close_db_connection():
    if sessionmanager._engine is not None:
        await sessionmanager.close()
