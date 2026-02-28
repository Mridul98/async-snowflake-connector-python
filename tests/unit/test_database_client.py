"""Unit tests for DatabaseClient."""
import pytest


class TestDatabaseClient:
    """Unit tests for DatabaseClient."""

    @pytest.mark.asyncio
    async def test_lazy_loading(self, mock_client):
        """Test database client is created lazily."""
        from async_snowflake.endpoints.databases import DatabaseClient
        db_client = mock_client.database
        assert isinstance(db_client, DatabaseClient)
