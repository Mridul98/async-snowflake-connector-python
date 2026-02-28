from typing import Optional, List
from .base import SnowflakeClient
from async_snowflake.data_structures.models.database import Database


class DatabaseClient:
    """Client for Snowflake Database operations."""

    def __init__(self, client: SnowflakeClient):
        self._client = client

    async def list(
        self,
        like: Optional[str] = None,
        show_limit: Optional[int] = None,
    ) -> List[Database]:
        """List all databases."""
        params = {}
        if like:
            params["like"] = like
        if show_limit:
            params["showLimit"] = show_limit

        response = await self._client._request(
            "GET",
            "/api/v2/databases",
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [Database(**db) for db in data]
        return [Database(**db) for db in data.get("databases", [])]

    async def create(
        self,
        name: str,
        kind: str = "PERMANENT",
        comment: Optional[str] = None,
    ) -> Database:
        """Create a new database."""
        body = {"name": name, "kind": kind}
        if comment:
            body["comment"] = comment

        response = await self._client._request(
            "POST",
            "/api/v2/databases",
            json=body,
        )
        response.raise_for_status()
        data = response.json()
        return Database(**data)

    async def drop(self, name: str) -> None:
        """Drop a database."""
        response = await self._client._request(
            "DELETE",
            f"/api/v2/databases/{name}",
        )
        response.raise_for_status()

    async def describe(self, name: str) -> Database:
        """Describe a database."""
        response = await self._client._request(
            "GET",
            f"/api/v2/databases/{name}",
        )
        response.raise_for_status()
        data = response.json()
        return Database(**data)
