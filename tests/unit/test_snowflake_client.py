"""Unit tests for SnowflakeClient."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from async_snowflake.endpoints.base import SnowflakeClient
from async_snowflake.endpoints.accounts import AccountClient
from async_snowflake.endpoints.databases import DatabaseClient
from async_snowflake.endpoints.schemas import SchemaClient
from async_snowflake.endpoints.tables import TableClient
from async_snowflake.endpoints.warehouses import WarehouseClient
from async_snowflake.endpoints.query import QueryClient


class TestSnowflakeClient:
    """Unit tests for SnowflakeClient."""

    @pytest.mark.asyncio
    async def test_create_factory_method(self, mock_auth_client):
        """Test factory method creates and initializes client."""
        mock_auth_client.initialize = AsyncMock()
        
        with patch('async_snowflake.endpoints.base.httpx.AsyncClient') as mock_httpx:
            mock_httpx.return_value = MagicMock()
            
            client = await SnowflakeClient.create(
                base_url="https://test.snowflakecomputing.com",
                auth_client=mock_auth_client,
            )
            
            assert client is not None
            mock_auth_client.initialize.assert_called_once()

    @pytest.mark.asyncio
    async def test_context_manager_close(self, mock_auth_client):
        """Test context manager closes properly."""
        mock_auth_client.initialize = AsyncMock()
        mock_auth_client.close = AsyncMock()
        
        with patch('async_snowflake.endpoints.base.httpx.AsyncClient') as mock_httpx:
            mock_http = MagicMock()
            mock_http.aclose = AsyncMock()
            mock_httpx.return_value = mock_http
            
            client = await SnowflakeClient.create(
                base_url="https://test.snowflakecomputing.com",
                auth_client=mock_auth_client,
            )
            await client.close()
            
            mock_http.aclose.assert_called_once()
            mock_auth_client.close.assert_called_once()

    @pytest.mark.asyncio
    async def test_lazy_loading_account_client(self, mock_client):
        """Test account client is created lazily."""
        account_client = mock_client.account
        assert isinstance(account_client, AccountClient)
        assert mock_client.account is account_client

    @pytest.mark.asyncio
    async def test_lazy_loading_database_client(self, mock_client):
        """Test database client is created lazily."""
        db_client = mock_client.database
        assert isinstance(db_client, DatabaseClient)
        assert mock_client.database is db_client

    @pytest.mark.asyncio
    async def test_lazy_loading_warehouse_client(self, mock_client):
        """Test warehouse client is created lazily."""
        wh_client = mock_client.warehouse
        assert isinstance(wh_client, WarehouseClient)
        assert mock_client.warehouse is wh_client

    @pytest.mark.asyncio
    async def test_lazy_loading_query_client(self, mock_client):
        """Test query client is created lazily."""
        query_client = mock_client.query
        assert isinstance(query_client, QueryClient)
        assert mock_client.query is query_client

    @pytest.mark.asyncio
    async def test_lazy_loading_schema_client(self, mock_client):
        """Test schema client is created lazily."""
        schema_client = mock_client.schema
        assert isinstance(schema_client, SchemaClient)
        assert mock_client.schema is schema_client

    @pytest.mark.asyncio
    async def test_lazy_loading_table_client(self, mock_client):
        """Test table client is created lazily."""
        table_client = mock_client.table
        assert isinstance(table_client, TableClient)
        assert mock_client.table is table_client
