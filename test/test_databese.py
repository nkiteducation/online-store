import pytest

from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from app.database.models import metadata


@pytest.mark.asyncio
async def test_database_connection(session: async_sessionmaker[AsyncSession]):
    async with session() as db_session:
        result = await db_session.execute(text("SELECT 1"))
        assert result.scalar() == 1


@pytest.mark.asyncio
async def test_chac_database(session: async_sessionmaker[AsyncSession]):
    async with session() as db_session:
        result = await db_session.execute(
            text("SELECT name FROM sqlite_master WHERE type='table';")
        )
        tables = result.scalars().all()
        assert list(metadata.tables.keys()) == tables
