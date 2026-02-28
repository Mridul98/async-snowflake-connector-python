"""Integration tests for TableClient."""
import pytest


class TestTableClientIntegration:
    """Integration tests for TableClient."""

    @pytest.mark.asyncio
    async def test_list_tables_via_query(self, snowflake_client):
        """Test listing tables via query."""
        result = await snowflake_client.query.execute(
            "SELECT TABLE_NAME FROM SNOWFLAKE_SAMPLE_DATA.INFORMATION_SCHEMA.TABLES LIMIT 5"
        )
        
        assert result.row_count == 5
        assert len(result.data) == 5
