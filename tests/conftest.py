import asyncio
import pytest
import pytest_asyncio
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.pool import StaticPool
from tests.factories import (
    UserFactory,
    DocumentFactory,
    DocumentSummaryFactory,
    ComparisonFactory,
    ComparisonDocumentFactory,
    UserHistoryFactory,
)

from app.db.base import Base


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def db_session():
    engine = create_async_engine(
        "sqlite+aiosqlite:///:memory:",
        poolclass=StaticPool,
    )

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    SessionLocal = async_sessionmaker(
        bind=engine,
        expire_on_commit=False,
        class_=AsyncSession,
    )

    async with SessionLocal() as session:
        yield session

    await engine.dispose()


@pytest_asyncio.fixture(autouse=True)
async def setup_factories(db_session):
    factories = [
        UserFactory,
        DocumentFactory,
        DocumentSummaryFactory,
        ComparisonFactory,
        ComparisonDocumentFactory,
        UserHistoryFactory,
    ]

    for factory_cls in factories:
        factory_cls._meta.sqlalchemy_session = db_session

    yield

    for factory_cls in factories:
        factory_cls._meta.sqlalchemy_session = None
