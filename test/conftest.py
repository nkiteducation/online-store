import os

from unittest import mock

import pytest
import pytest_asyncio

from httpx import ASGITransport, AsyncClient

from app.main import app
from loguru import logger


@pytest_asyncio.fixture
async def client():
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as client:
        yield client


@pytest.fixture(scope="session", autouse=True)
def env_setup():
    with mock.patch.dict(
        os.environ,
        values={
            "DEVELOPMENT": "true",
            "API_HOST": "0.0.0.0",
            "API_PORT": "0000",
            "API_WORKERS": "4",
        },
        clear=True,
    ):
        logger.debug(f"ENV: {os.environ.copy()}")
        yield
