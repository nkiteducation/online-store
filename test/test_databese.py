from typing import Literal

import pytest
from faker import Faker
from sqlalchemy import insert, text
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.models import User, metadata


@pytest.fixture(scope="session")
def user_deta(faker: Faker) -> dict[Literal["name", "email", "password"], any]:
    return {
        "name": faker.name(),
        "email": faker.email(),
        "password": faker.password().encode("utf-8"),
    }


@pytest.mark.asyncio
async def test_database_connection(session: AsyncSession) -> None:
    result = await session.execute(text("SELECT 1"))
    assert result.scalar() == 1


@pytest.mark.asyncio
async def test_chac_database(session: AsyncSession) -> None:
    result = await session.execute(
        text("SELECT name FROM sqlite_master WHERE type='table';"),
    )
    tables = result.scalars().all()
    assert list(metadata.tables.keys()) == tables


@pytest.mark.asyncio
async def test_user(session: AsyncSession, user_deta) -> None:
    request = insert(User).values(**user_deta).returning(User)
    response = await session.execute(request)
    user = response.scalar()

    assert user.name == user_deta["name"]
    assert user.email == user_deta["email"]
    assert user.password == user_deta["password"]
