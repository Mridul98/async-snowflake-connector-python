"""Integration tests for QueryClient."""
import asyncio

import pytest


class TestQueryClientAsyncIntegration:
    """Integration tests for the async query path: execute_async -> get_results."""

    @pytest.mark.asyncio
    async def test_execute_async_returns_handle(self, snowflake_client):
        """execute_async submits and returns a statement handle string (issue #4)."""
        handle = await snowflake_client.query.execute_async("SELECT 1 AS N")

        assert isinstance(handle, str)
        assert handle  # non-empty

    @pytest.mark.asyncio
    async def test_get_status_reports_terminal_state(self, snowflake_client):
        """get_status polls without crashing and reaches a terminal state (issue #5)."""
        handle = await snowflake_client.query.execute_async("SELECT 1 AS N")

        status = None
        for _ in range(30):
            status = await snowflake_client.query.get_status(handle)
            assert status.state in ("running", "success")
            if status.state != "running":
                break
            await asyncio.sleep(1.0)

        assert status is not None
        assert status.state == "success"

    @pytest.mark.asyncio
    async def test_async_roundtrip_results(self, snowflake_client):
        """Full round-trip: submit, poll, fetch results with correct metadata (issue #6)."""
        handle = await snowflake_client.query.execute_async(
            "SELECT SEQ4() AS N FROM TABLE(GENERATOR(ROWCOUNT => 5))"
        )

        for _ in range(30):
            status = await snowflake_client.query.get_status(handle)
            if status.state != "running":
                break
            await asyncio.sleep(1.0)

        result = await snowflake_client.query.get_results(handle)

        assert result.query_state == "success"
        assert result.columns == ["N"]
        assert result.row_count == 5
        assert len(result.rows) == 5

    @pytest.mark.asyncio
    async def test_async_results_fetches_all_partitions(self, snowflake_client):
        """Large results span multiple partitions and must not be truncated (issue #6)."""
        handle = await snowflake_client.query.execute_async(
            "SELECT SEQ4() AS N FROM TABLE(GENERATOR(ROWCOUNT => 50000))"
        )

        for _ in range(60):
            status = await snowflake_client.query.get_status(handle)
            if status.state != "running":
                break
            await asyncio.sleep(1.0)

        result = await snowflake_client.query.get_results(handle)

        assert result.row_count == 50000
        # rows are concatenated across all partitions, not just the first
        assert len(result.rows) == 50000


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
