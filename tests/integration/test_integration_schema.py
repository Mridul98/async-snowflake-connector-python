"""Integration tests for SchemaClient."""
import pytest


class TestSchemaClientIntegration:
    """Integration tests for SchemaClient."""

    @pytest.mark.asyncio
    async def test_list_schemas_in_database(self, snowflake_client):
        """Test listing schemas in a specific database."""
        result = await snowflake_client.schema.list(database="SNOWFLAKE")
        
        assert isinstance(result, list)
