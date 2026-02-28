"""Unit tests for SchemaClient."""
import pytest


class TestSchemaClient:
    """Unit tests for SchemaClient."""

    @pytest.mark.asyncio
    async def test_lazy_loading(self, mock_client):
        """Test schema client is created lazily."""
        from async_snowflake.endpoints.schemas import SchemaClient
        schema_client = mock_client.schema
        assert isinstance(schema_client, SchemaClient)
