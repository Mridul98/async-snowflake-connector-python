from typing import Optional, List
from .base import SnowflakeClient
from async_snowflake.data_structures.models.table import SnowflakeTable


class TableClient:
    """Client for Snowflake Table operations."""

    def __init__(self, client: SnowflakeClient):
        self._client = client

    async def list(
        self,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        like: Optional[str] = None,
        show_limit: Optional[int] = None,
    ) -> List[SnowflakeTable]:
        """List all tables."""
        params = {}
        if like:
            params["like"] = like
        if show_limit:
            params["showLimit"] = show_limit

        if database and schema:
            path = f"/api/v2/databases/{database}/schemas/{schema}/tables"
        elif database:
            path = f"/api/v2/databases/{database}/tables"
        else:
            path = "/api/v2/tables"

        response = await self._client._request("GET", path, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            return [SnowflakeTable(**t) for t in data]
        return [SnowflakeTable(**t) for t in data.get("tables", [])]

    async def describe(
        self,
        name: str,
        database: str,
        schema: str,
    ) -> SnowflakeTable:
        """Describe a table."""
        response = await self._client._request(
            "GET",
            f"/api/v2/databases/{database}/schemas/{schema}/tables/{name}",
        )
        response.raise_for_status()
        data = response.json()
        return SnowflakeTable(**data)

    async def get_columns(
        self,
        name: str,
        database: str,
        schema: str,
    ) -> List[dict]:
        """Get columns of a table."""
        response = await self._client._request(
            "GET",
            f"/api/v2/databases/{database}/schemas/{schema}/tables/{name}/columns",
        )
        response.raise_for_status()
        data = response.json()
        return data.get("columns", [])
