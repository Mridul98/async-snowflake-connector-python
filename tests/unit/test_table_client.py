"""Unit tests for TableClient."""
import pytest


class TestTableClient:
    """Unit tests for TableClient."""

    @pytest.mark.asyncio
    async def test_lazy_loading(self, mock_client):
        """Test table client is created lazily."""
        from async_snowflake.endpoints.tables import TableClient
        table_client = mock_client.table
        assert isinstance(table_client, TableClient)
