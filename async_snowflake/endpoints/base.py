from __future__ import annotations

import httpx
from typing import Optional, TYPE_CHECKING

from async_snowflake.authentication.auth_clients import SnowflakeBaseAuthClient

if TYPE_CHECKING:
    from async_snowflake.endpoints.accounts import AccountClient
    from async_snowflake.endpoints.databases import DatabaseClient
    from async_snowflake.endpoints.schemas import SchemaClient
    from async_snowflake.endpoints.tables import TableClient
    from async_snowflake.endpoints.warehouses import WarehouseClient
    from async_snowflake.endpoints.query import QueryClient


class SnowflakeClient:
    """
    Main async client for Snowflake interactions.

    Usage:
        client = await SnowflakeClient.create(
            base_url="https://account.snowflakecomputing.com",
            auth_client=auth
        )

        async with SnowflakeClient.create(base_url, auth) as client:
            result = await client.query.execute("SELECT 1")

    Fluent interface:
        client.account.get_current_account()
        client.database.list()
        client.warehouse.resume("warehouse_name")
        client.query.execute("SELECT * FROM table")
    """

    def __init__(
        self,
        base_url: str,
        auth_client: SnowflakeBaseAuthClient,
        timeout: float = 60.0,
    ):
        self._base_url = base_url.rstrip("/")
        self._auth_client = auth_client
        self._timeout = timeout
        self._http_client: Optional[httpx.AsyncClient] = None

        self._account: Optional[AccountClient] = None
        self._database: Optional[DatabaseClient] = None
        self._schema: Optional[SchemaClient] = None
        self._table: Optional[TableClient] = None
        self._warehouse: Optional[WarehouseClient] = None
        self._query: Optional[QueryClient] = None

    @classmethod
    async def create(
        cls,
        base_url: str,
        auth_client: SnowflakeBaseAuthClient,
        timeout: float = 60.0,
    ) -> SnowflakeClient:
        """Factory method to create and initialize the client."""
        client = cls(base_url, auth_client, timeout)
        await client._initialize()
        return client

    async def _initialize(self):
        """Initialize the HTTP client."""
        self._http_client = httpx.AsyncClient(
            timeout=self._timeout,
            limits=httpx.Limits(max_keepalive_connections=10, max_connections=20),
        )
        if hasattr(self._auth_client, "initialize"):
            await self._auth_client.initialize()

    async def __aenter__(self) -> SnowflakeClient:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()

    async def close(self):
        """Close the client and release resources."""
        if self._http_client:
            await self._http_client.aclose()
            self._http_client = None
        if hasattr(self._auth_client, "close"):
            await self._auth_client.close()

    async def _request(
        self,
        method: str,
        path: str,
        **kwargs,
    ) -> httpx.Response:
        """Make an HTTP request with auth refresh."""
        token = await self._auth_client.get_token()
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
        }
        url = f"{self._base_url}{path}"
        return await self._http_client.request(method, url, headers=headers, **kwargs)

    @property
    def account(self) -> AccountClient:
        """Account operations."""
        from async_snowflake.endpoints.accounts import AccountClient

        if self._account is None:
            self._account = AccountClient(self)
        return self._account

    @property
    def database(self) -> DatabaseClient:
        """Database operations."""
        from async_snowflake.endpoints.databases import DatabaseClient

        if self._database is None:
            self._database = DatabaseClient(self)
        return self._database

    @property
    def schema(self) -> SchemaClient:
        """Schema operations."""
        from async_snowflake.endpoints.schemas import SchemaClient

        if self._schema is None:
            self._schema = SchemaClient(self)
        return self._schema

    @property
    def table(self) -> TableClient:
        """Table operations."""
        from async_snowflake.endpoints.tables import TableClient

        if self._table is None:
            self._table = TableClient(self)
        return self._table

    @property
    def warehouse(self) -> WarehouseClient:
        """Warehouse operations."""
        from async_snowflake.endpoints.warehouses import WarehouseClient

        if self._warehouse is None:
            self._warehouse = WarehouseClient(self)
        return self._warehouse

    @property
    def query(self) -> QueryClient:
        """Query execution operations."""
        from async_snowflake.endpoints.query import QueryClient

        if self._query is None:
            self._query = QueryClient(self)
        return self._query
