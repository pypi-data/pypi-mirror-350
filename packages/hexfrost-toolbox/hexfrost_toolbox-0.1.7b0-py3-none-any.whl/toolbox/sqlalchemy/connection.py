import dataclasses
import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.pool import NullPool

logger = logging.getLogger(__name__)


@dataclasses.dataclass
class DatabaseConnectionSettings:
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DB: str
    SCHEMA_MAPPING: dict | None = None

    def get_dsn(self):
        dsn = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
        return dsn


class DatabaseConnectionManager:
    def __init__(self, settings: DatabaseConnectionSettings):
        self._engine = None
        self._async_sessionmaker = None
        self._settings = settings
        self._schema_mapping = {None: "public", "public": "public"}
        if settings.SCHEMA_MAPPING:
            self._schema_mapping.update(settings.SCHEMA_MAPPING)

    def _get_settings(self):
        if not self._settings:
            raise RuntimeError("No settings available")
        return self._settings

    def set_engine(self, engine: AsyncEngine):
        self._engine = engine

    def get_engine(self) -> AsyncEngine:
        if not self._engine:
            s = self._settings
            db_host = s.POSTGRES_HOST
            self._engine = create_async_engine(
                f"postgresql+asyncpg://{s.POSTGRES_USER}:{s.POSTGRES_PASSWORD}@{db_host}:{s.POSTGRES_PORT}/{s.POSTGRES_DB}",
                poolclass=NullPool,
            ).execution_options(schema_translate_map=self._schema_mapping)
        return self._engine

    def get_session_maker(self):
        if not self._async_sessionmaker:
            self._async_sessionmaker = async_sessionmaker(
                self.get_engine(),
                expire_on_commit=False,
                class_=AsyncSession,
            )
        return self._async_sessionmaker

    @asynccontextmanager
    async def get_db_session(self) -> AsyncGenerator[AsyncSession, None]:
        session_maker = self.get_session_maker()
        async with session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                logger.error({"mgs": e})
                await session.rollback()
                raise
            finally:
                await session.close()

    async def __call__(self):
        session_maker = self.get_session_maker()
        async with session_maker() as session:
            try:
                yield session
                await session.commit()
            except Exception as e:
                logger.error({"mgs": e})
                await session.rollback()
                raise
            finally:
                await session.close()


__all__ = ["DatabaseConnectionManager", "DatabaseConnectionSettings"]
