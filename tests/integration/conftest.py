"""Integration test fixtures."""
import pytest
import asyncio

from async_snowflake import SnowflakeClient, SnowflakeJWTAuthClient, CredentialsManager


def get_test_credentials():
    """Get test credentials from TOML or environment."""
    try:
        manager = CredentialsManager(profile="default")
        return manager.credentials
    except (FileNotFoundError, KeyError, ValueError):
        return CredentialsManager.from_environment()


TEST_CREDS = get_test_credentials()


@pytest.fixture(scope="session")
def event_loop():
    """Create event loop for session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def auth_client():
    """Create actual auth client for integration tests."""
    client = SnowflakeJWTAuthClient(
        account=TEST_CREDS.account,
        user=TEST_CREDS.user,
        private_key_path=TEST_CREDS.private_key_path,
    )
    await client.initialize()
    yield client
    await client.close()


@pytest.fixture
async def snowflake_client(auth_client):
    """Create actual Snowflake client for integration tests."""
    client = await SnowflakeClient.create(
        base_url=TEST_CREDS.base_url,
        auth_client=auth_client,
    )
    yield client
    await client.close()
