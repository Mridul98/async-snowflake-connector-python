"""Unit tests for QueryClient."""
import pytest
from async_snowflake.endpoints.query import QueryResult


class TestQueryClient:
    """Unit tests for QueryClient."""

    @pytest.mark.asyncio
    async def test_lazy_loading(self, mock_client):
        """Test query client is created lazily."""
        from async_snowflake.endpoints.query import QueryClient
        query_client = mock_client.query
        assert isinstance(query_client, QueryClient)


class TestQueryResult:
    """Unit tests for QueryResult class."""

    def test_iteration(self):
        """Test QueryResult iteration."""
        result = QueryResult(
            query_id="test_id",
            data=[["a", "b"], ["c", "d"]],
            columns=["col1", "col2"],
            row_count=2,
            status="success"
        )
        
        rows = list(result)
        assert len(rows) == 2

    def test_length(self):
        """Test QueryResult length."""
        result = QueryResult(
            query_id="test_id",
            data=[["a"], ["b"], ["c"]],
            columns=["col1"],
            row_count=3,
            status="success"
        )
        
        assert len(result) == 3
