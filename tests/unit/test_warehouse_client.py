"""Unit tests for WarehouseClient."""
import pytest


class TestWarehouseClient:
    """Unit tests for WarehouseClient."""

    @pytest.mark.asyncio
    async def test_lazy_loading(self, mock_client):
        """Test warehouse client is created lazily."""
        from async_snowflake.endpoints.warehouses import WarehouseClient
        wh_client = mock_client.warehouse
        assert isinstance(wh_client, WarehouseClient)
