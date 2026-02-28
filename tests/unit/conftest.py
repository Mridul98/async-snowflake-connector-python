"""Unit test fixtures."""
import pytest
from unittest.mock import AsyncMock

from async_snowflake import SnowflakeClient, SnowflakeJWTAuthClient


@pytest.fixture
def mock_auth_client():
    """Create a mock auth client."""
    mock = AsyncMock(spec=SnowflakeJWTAuthClient)
    mock.get_token = AsyncMock(return_value="mock_token")
    mock.initialize = AsyncMock()
    mock.close = AsyncMock()
    return mock


@pytest.fixture
async def mock_client(mock_auth_client):
    """Create a client with mocked HTTP client."""
    client = SnowflakeClient(
        base_url="https://test.snowflakecomputing.com",
        auth_client=mock_auth_client,
    )
    mock_http = AsyncMock()
    mock_http.request = AsyncMock()
    client._http_client = mock_http
    return client
