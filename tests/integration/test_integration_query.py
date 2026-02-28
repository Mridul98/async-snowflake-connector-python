"""Integration tests for QueryClient."""
import pytest


class TestQueryClientIntegration:
    """Integration tests for QueryClient."""

    @pytest.mark.asyncio
    async def test_execute_simple_query(self, snowflake_client):
        """Test executing a simple query."""
        result = await snowflake_client.query.execute("SELECT 1 as test")
        
        assert result is not None
        assert result.query_id is not None
        assert result.status == "success"
        assert result.row_count == 1
        assert result.columns == ["TEST"]
        assert result.data == [["1"]]

    @pytest.mark.asyncio
    async def test_execute_query_with_columns(self, snowflake_client):
        """Test executing a query with multiple columns."""
        result = await snowflake_client.query.execute("SELECT 1 as a, 2 as b, 3 as c")
        
        assert result.columns == ["A", "B", "C"]
        assert result.row_count == 1

    @pytest.mark.asyncio
    async def test_execute_query_with_database(self, snowflake_client):
        """Test executing a query with database context."""
        result = await snowflake_client.query.execute(
            "SELECT CURRENT_DATABASE() as db",
            database="SNOWFLAKE"
        )
        
        assert result is not None
        assert result.status == "success"

    @pytest.mark.asyncio
    async def test_query_result_iteration(self, snowflake_client):
        """Test QueryResult iteration."""
        result = await snowflake_client.query.execute("SELECT * FROM (SELECT 1 as a UNION ALL SELECT 2)")

        rows = list(result)
        assert len(rows) == 2

    @pytest.mark.asyncio
    async def test_query_result_length(self, snowflake_client):
        """Test QueryResult length."""
        result = await snowflake_client.query.execute("SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3")

        assert len(result) == 3
