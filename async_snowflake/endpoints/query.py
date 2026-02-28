from typing import Optional, List
from .base import SnowflakeClient
from async_snowflake.data_structures.models.query import (
    QueryResult,
    QueryStatus,
    QueryHistoryEntry,
)


class QueryClient:
    """Client for Snowflake Query operations."""

    def __init__(self, client: SnowflakeClient):
        self._client = client

    async def execute(
        self,
        sql: str,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        warehouse: Optional[str] = None,
        timeout: Optional[float] = None,
    ) -> QueryResult:
        """
        Execute a synchronous query and return results.

        Args:
            sql: The SQL query to execute
            database: Database to use
            schema: Schema to use
            warehouse: Warehouse to use
            timeout: Query timeout in seconds

        Returns:
            QueryResult with rows and metadata
        """
        params = {"statement": sql}
        if database:
            params["database"] = database
        if schema:
            params["schema"] = schema
        if warehouse:
            params["warehouse"] = warehouse
        if timeout:
            params["timeout"] = int(timeout)

        response = await self._client._request(
            "POST",
            "/api/v2/statements",
            json=params,
        )
        response.raise_for_status()
        data = response.json()

        meta = data.get("resultSetMetaData", {})
        row_type = meta.get("rowType", [])
        column_names = [col.get("name") for col in row_type] if row_type else []

        query_status = "success" if "data" in data else data.get("status", "unknown")

        return QueryResult(
            rows=data.get("data", []),
            columns=column_names,
            row_count=meta.get("numRows"),
            query_id=data.get("statementHandle"),
            query_state=query_status,
        )

    async def execute_async(
        self,
        sql: str,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        warehouse: Optional[str] = None,
    ) -> str:
        """
        Execute a query asynchronously and return the query ID.

        Args:
            sql: The SQL query to execute
            database: Database to use
            schema: Schema to use
            warehouse: Warehouse to use

        Returns:
            Query ID for polling status
        """
        params = {
            "statement": sql,
            "asyncExecution": True,
        }
        if database:
            params["database"] = database
        if schema:
            params["schema"] = schema
        if warehouse:
            params["warehouse"] = warehouse

        response = await self._client._request(
            "POST",
            "/api/v2/statements",
            json=params,
        )
        response.raise_for_status()
        data = response.json()

        return data.get("statementHandle")

    async def get_status(self, query_id: str) -> QueryStatus:
        """
        Get the status of a query.

        Args:
            query_id: The query ID to check

        Returns:
            QueryStatus with current state
        """
        response = await self._client._request(
            "GET",
            f"/api/v2/statements/{query_id}",
        )
        response.raise_for_status()
        data = response.json()

        return QueryStatus(
            query_id=query_id,
            state=data.get("status"),
            error_message=data.get("errorMessage"),
            row_count=data.get("rowCount"),
        )

    async def get_results(self, query_id: str) -> QueryResult:
        """
        Get the results of a completed query.

        Args:
            query_id: The query ID to get results for

        Returns:
            QueryResult with rows and metadata
        """
        response = await self._client._request(
            "GET",
            f"/api/v2/statements/{query_id}",
        )
        response.raise_for_status()
        data = response.json()

        return QueryResult(
            rows=data.get("data", []),
            columns=data.get("columns", []),
            row_count=data.get("rowCount"),
            query_id=query_id,
            query_state=data.get("status"),
        )

    async def cancel(self, query_id: str) -> bool:
        """
        Cancel a running query.

        Args:
            query_id: The query ID to cancel

        Returns:
            True if cancelled successfully
        """
        response = await self._client._request(
            "POST",
            f"/api/v2/statements/{query_id}/cancel",
        )
        response.raise_for_status()
        data = response.json()

        return data.get("canceled", False)

    async def get_history(
        self,
        user: Optional[str] = None,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        limit: Optional[int] = 100,
    ) -> List[QueryHistoryEntry]:
        """
        Get query history.

        Args:
            user: Filter by user
            database: Filter by database
            schema: Filter by schema
            limit: Maximum number of entries to return

        Returns:
            List of query history entries
        """
        params = {"limit": limit}
        if user:
            params["userName"] = user
        if database:
            params["databaseName"] = database
        if schema:
            params["schemaName"] = schema

        response = await self._client._request(
            "GET",
            "/api/v2/statements",
            params=params,
        )
        response.raise_for_status()
        data = response.json()

        statements = data.get("statements", [])
        return [QueryHistoryEntry(**entry) for entry in statements]
