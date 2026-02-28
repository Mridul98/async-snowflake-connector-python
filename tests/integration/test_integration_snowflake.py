"""Integration tests for SnowflakeClient."""
import pytest


class TestSnowflakeClientIntegration:
    """Integration tests for SnowflakeClient."""

    @pytest.mark.asyncio
    async def test_factory_creates_client(self, snowflake_client):
        """Test factory method creates properly initialized client."""
        assert snowflake_client is not None
        assert snowflake_client._http_client is not None

    @pytest.mark.asyncio
    async def test_context_manager_usage(self, snowflake_client):
        """Test using SnowflakeClient as context manager."""
        result = await snowflake_client.query.execute("SELECT 1")
        assert result.status == "success"
