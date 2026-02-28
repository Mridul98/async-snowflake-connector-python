"""Integration tests for WarehouseClient."""
import pytest


class TestWarehouseClientIntegration:
    """Integration tests for WarehouseClient."""

    @pytest.mark.asyncio
    async def test_list_warehouses(self, snowflake_client):
        """Test listing warehouses."""
        result = await snowflake_client.warehouse.list()
        
        assert isinstance(result, list)
        assert len(result) > 0
        wh = result[0]
        assert hasattr(wh, 'name')
        assert hasattr(wh, 'warehouse_size')

    @pytest.mark.asyncio
    async def test_describe_warehouse(self, snowflake_client):
        """Test describing a warehouse."""
        warehouses = await snowflake_client.warehouse.list()
        if warehouses:
            result = await snowflake_client.warehouse.describe(warehouses[0].name)
            assert result.name == warehouses[0].name
