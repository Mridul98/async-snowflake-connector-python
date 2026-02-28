"""Integration tests for DatabaseClient."""
import pytest


class TestDatabaseClientIntegration:
    """Integration tests for DatabaseClient."""

    @pytest.mark.asyncio
    async def test_list_databases(self, snowflake_client):
        """Test listing databases."""
        result = await snowflake_client.database.list()
        
        assert isinstance(result, list)
        assert len(result) > 0
        db = result[0]
        assert hasattr(db, 'name')
        assert hasattr(db, 'kind')

    @pytest.mark.asyncio
    async def test_list_databases_with_params(self, snowflake_client):
        """Test listing databases with filter params."""
        result = await snowflake_client.database.list(like="SNOWFLAKE%", show_limit=5)
        
        assert isinstance(result, list)

    @pytest.mark.asyncio
    async def test_describe_database(self, snowflake_client):
        """Test describing a database."""
        result = await snowflake_client.database.describe("SNOWFLAKE_LEARNING_DB")
        
        assert result.name == "SNOWFLAKE_LEARNING_DB"
        assert hasattr(result, 'kind')
