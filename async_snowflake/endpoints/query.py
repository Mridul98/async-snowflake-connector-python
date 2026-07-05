import asyncio
from typing import Optional, List, Any, AsyncIterator

import httpx

from .base import SnowflakeClient
from async_snowflake.data_structures.models.query import (
    QueryResult,
    QueryStatus,
    QueryHistoryEntry,
)

# Transient transport failures worth retrying: a keep-alive connection closed
# between requests surfaces as RemoteProtocolError/ReadError; ConnectError
# covers a failed re-dial. A fresh attempt gets a new connection.
_RETRYABLE_ERRORS = (
    httpx.RemoteProtocolError,
    httpx.ReadError,
    httpx.ConnectError,
)


class QueryClient:
    """Client for Snowflake Query operations."""

    def __init__(self, client: SnowflakeClient):
        self._client = client

    async def _get_json_with_retry(
        self,
        path: str,
        *,
        attempts: int = 3,
        **kwargs,
    ) -> dict:
        """GET ``path`` and return the parsed JSON body, retrying transient
        transport errors with exponential backoff.

        Partition/statement GETs are idempotent, so retrying is safe. Only
        transport-level drops (see ``_RETRYABLE_ERRORS``) are retried; HTTP
        error statuses still raise immediately via ``raise_for_status()``.
        """
        for attempt in range(attempts):
            try:
                response = await self._client._request("GET", path, **kwargs)
                response.raise_for_status()
                return response.json()
            except _RETRYABLE_ERRORS:
                if attempt == attempts - 1:
                    raise
                await asyncio.sleep(0.5 * (2**attempt))

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
        body = {"statement": sql}
        if database:
            body["database"] = database
        if schema:
            body["schema"] = schema
        if warehouse:
            body["warehouse"] = warehouse

        response = await self._client._request(
            "POST",
            "/api/v2/statements",
            params={"async": "true"},
            json=body,
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

        # SQL API v2 does not return a "status" field. An in-progress statement
        # comes back as HTTP 202 (code 333334) and a finished one as HTTP 200
        # (code 090001) with resultSetMetaData. Derive state from the HTTP
        # status; row count lives under resultSetMetaData.numRows.
        state = "running" if response.status_code == 202 else "success"
        meta = data.get("resultSetMetaData", {})

        return QueryStatus(
            query_id=query_id,
            state=state,
            error_message=None,
            row_count=meta.get("numRows"),
        )

    async def get_results(self, query_id: str) -> QueryResult:
        """
        Get the results of a completed query.

        Args:
            query_id: The query ID to get results for

        Returns:
            QueryResult with rows and metadata
        """
        data = await self._get_json_with_retry(f"/api/v2/statements/{query_id}")

        # Parse resultSetMetaData the same way execute() does: the SQL API v2
        # response has no top-level "columns"/"rowCount"/"status" keys.
        meta = data.get("resultSetMetaData", {})
        row_type = meta.get("rowType", [])
        column_names = [col.get("name") for col in row_type] if row_type else []

        rows = list(data.get("data", []) or [])

        # Large result sets are split into partitions: the first partition is
        # inline in "data", the rest must be fetched with ?partition=N. Each
        # fetch is retried on transient transport drops so one closed keep-alive
        # connection does not abort the whole result (see issue #9).
        partitions = meta.get("partitionInfo", []) or []
        for idx in range(1, len(partitions)):
            part_data = await self._get_json_with_retry(
                f"/api/v2/statements/{query_id}",
                params={"partition": idx},
            )
            rows.extend(part_data.get("data", []) or [])

        query_state = "success" if "data" in data else "unknown"

        return QueryResult(
            rows=rows,
            columns=column_names,
            row_count=meta.get("numRows"),
            query_id=query_id,
            query_state=query_state,
        )

    async def generate_results(self, query_id: str) -> AsyncIterator[List[List[Any]]]:
        """
        Stream the results of a completed query one partition at a time.

        Unlike :meth:`get_results`, which materializes every partition into a
        single list, this async generator fetches one partition at a time and
        yields it as a batch of rows, keeping memory bounded for large result
        sets. The first partition is inline in the initial response; the rest
        are fetched with ?partition=N. Each fetch is retried on transient
        transport drops (#9). Empty partitions are skipped.

        Args:
            query_id: The query ID to stream results for

        Yields:
            One partition at a time as a list of rows (each row a list of
            column values).

        Usage:
            async for partition in client.query.generate_results(handle):
                for row in partition:
                    process(row)
        """
        data = await self._get_json_with_retry(f"/api/v2/statements/{query_id}")

        first = data.get("data", []) or []
        if first:
            yield first

        meta = data.get("resultSetMetaData", {})
        partitions = meta.get("partitionInfo", []) or []
        for idx in range(1, len(partitions)):
            part_data = await self._get_json_with_retry(
                f"/api/v2/statements/{query_id}",
                params={"partition": idx},
            )
            batch = part_data.get("data", []) or []
            if batch:
                yield batch

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
