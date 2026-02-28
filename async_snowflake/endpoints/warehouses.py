from typing import Optional, List
from .base import SnowflakeClient
from async_snowflake.data_structures.models.warehouse import SnowflakeWarehouse


class WarehouseClient:
    """Client for Snowflake Warehouse operations."""

    def __init__(self, client: SnowflakeClient):
        self._client = client

    async def list(
        self,
        like: Optional[str] = None,
        show_limit: Optional[int] = None,
    ) -> List[SnowflakeWarehouse]:
        """List all warehouses."""
        params = {}
        if like:
            params["like"] = like
        if show_limit:
            params["showLimit"] = show_limit

        response = await self._client._request(
            "GET",
            "/api/v2/warehouses",
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [SnowflakeWarehouse(**w) for w in data]
        return [SnowflakeWarehouse(**w) for w in data.get("warehouses", [])]

    async def create(
        self,
        name: str,
        warehouse_size: str = "SMALL",
        comment: Optional[str] = None,
    ) -> SnowflakeWarehouse:
        """Create a new warehouse."""
        body = {"name": name, "warehouse_size": warehouse_size}
        if comment:
            body["comment"] = comment

        response = await self._client._request(
            "POST",
            "/api/v2/warehouses",
            json=body,
        )
        response.raise_for_status()
        data = response.json()
        return SnowflakeWarehouse(**data)

    async def drop(self, name: str) -> None:
        """Drop a warehouse."""
        response = await self._client._request(
            "DELETE",
            f"/api/v2/warehouses/{name}",
        )
        response.raise_for_status()

    async def resume(self, name: str) -> SnowflakeWarehouse:
        """Resume a suspended warehouse."""
        response = await self._client._request(
            "POST",
            f"/api/v2/warehouses/{name}/resume",
        )
        response.raise_for_status()
        data = response.json()
        return SnowflakeWarehouse(**data)

    async def suspend(self, name: str) -> SnowflakeWarehouse:
        """Suspend a running warehouse."""
        response = await self._client._request(
            "POST",
            f"/api/v2/warehouses/{name}/suspend",
        )
        response.raise_for_status()
        data = response.json()
        return SnowflakeWarehouse(**data)

    async def describe(self, name: str) -> SnowflakeWarehouse:
        """Describe a warehouse."""
        response = await self._client._request(
            "GET",
            f"/api/v2/warehouses/{name}",
        )
        response.raise_for_status()
        data = response.json()
        return SnowflakeWarehouse(**data)
