import os
import sys

from unittest import mock

import pytest
import pytest_asyncio

from httpx import ASGITransport, AsyncClient
from loguru import logger
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    async_sessionmaker,
    create_async_engine,
)

os.environ["PYTHONPATH"] = ".:./app"
from app.database.models import CoreModel
from app.main import app

logger.remove()
logger.add(sys.stderr, level="DEBUG", colorize=True)


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def setup_env():
    with mock.patch.dict(
        os.environ,
        values={
            "DEVELOPMENT": "true",
            "API_HOST": "0.0.0.0",
            "API_PORT": "0000",
            "API_WORKERS": "4",
            "DATABASE_POOL_SIZE": "5",
            "DATABASE_MAX_OVERFLOW": "10",
            "DATABASE_POOL_TIMEOUT": "30",
            "DATABASE_URL_DRIVERNAME": "postgresql+asyncpg",
            "DATABASE_URL_USERNAME": "postgres",
            "DATABASE_URL_PASSWORD": "password",
            "DATABASE_URL_HOST": "localhost",
            "DATABASE_URL_PORT": "5432",
            "DATABASE_URL_DATABASE": "postgres",
        },
        clear=True,
    ):
        yield


@pytest.fixture(scope="session")
def engine():
    return create_async_engine("sqlite+aiosqlite:///:memory:", future=True)


@pytest.fixture(scope="session")
def session(engine):
    return async_sessionmaker(bind=engine, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
async def setup_database(engine: AsyncEngine):
    async with engine.begin() as conn:
        await conn.run_sync(CoreModel.metadata.create_all)
    yield
    async with engine.begin() as conn:
        await conn.run_sync(CoreModel.metadata.drop_all)
