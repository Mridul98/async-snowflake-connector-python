from typing import Optional, List
from .base import SnowflakeClient
from async_snowflake.data_structures.models.schema import SchemaRead


class SchemaClient:
    """Client for Snowflake Schema operations."""

    def __init__(self, client: SnowflakeClient):
        self._client = client

    async def list(
        self,
        database: Optional[str] = None,
        like: Optional[str] = None,
        show_limit: Optional[int] = None,
    ) -> List[SchemaRead]:
        """List all schemas."""
        params = {}
        if like:
            params["like"] = like
        if show_limit:
            params["showLimit"] = show_limit

        if database:
            path = f"/api/v2/databases/{database}/schemas"
        else:
            path = "/api/v2/databases"

        response = await self._client._request("GET", path, params=params)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list):
            if database:
                schemas = []
                for db in data:
                    if "schemas" in db:
                        schemas.extend(db["schemas"])
                return [SchemaRead(**s) for s in schemas]
            return [SchemaRead(**s) for s in data]
        return [SchemaRead(**s) for s in data.get("schemas", [])]

    async def create(
        self,
        name: str,
        database: str,
        comment: Optional[str] = None,
    ) -> SchemaRead:
        """Create a new schema."""
        body = {"name": name}
        if comment:
            body["comment"] = comment

        response = await self._client._request(
            "POST",
            f"/api/v2/databases/{database}/schemas",
            json=body,
        )
        response.raise_for_status()
        data = response.json()
        return SchemaRead(**data)

    async def drop(self, name: str, database: str) -> None:
        """Drop a schema."""
        response = await self._client._request(
            "DELETE",
            f"/api/v2/databases/{database}/schemas/{name}",
        )
        response.raise_for_status()

    async def describe(self, name: str, database: str) -> SchemaRead:
        """Describe a schema."""
        response = await self._client._request(
            "GET",
            f"/api/v2/databases/{database}/schemas/{name}",
        )
        response.raise_for_status()
        data = response.json()
        return SchemaRead(**data)
