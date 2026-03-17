from collections.abc import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
    AsyncEngine,
)

from app.core.config import settings

engine: AsyncEngine = create_async_engine(
    settings.db_url, echo=False, pool_pre_ping=True
)
FactorySession: async_sessionmaker[AsyncSession] = async_sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)


async def engine_dispose():
    await engine.dispose()


async def get_sesion() -> AsyncGenerator[AsyncSession, None]:
    async with FactorySession() as session:
        yield session
