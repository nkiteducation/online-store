from httpx import AsyncClient
import pytest

@pytest.mark.asyncio
async def test_health(client: AsyncClient):
    response = await client.get("/health")
    assert response.status_code == 204
    assert response.text == ""