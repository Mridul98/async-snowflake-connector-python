from typing import Optional, List
from .base import SnowflakeClient
from async_snowflake.data_structures.models.account import SnowflakeAccount


class AccountClient:
    """Client for Snowflake Account operations."""
    
    def __init__(self, client: SnowflakeClient):
        self._client = client
    
    async def get_current_account(self) -> SnowflakeAccount:
        """Get the current account details."""
        response = await self._client._request("GET", "/api/v2/account")
        response.raise_for_status()
        data = response.json()
        return SnowflakeAccount(**data)
    
    async def list_accounts(
        self,
        like: Optional[str] = None,
        show_limit: Optional[int] = None,
    ) -> List[SnowflakeAccount]:
        """List all accounts in the organization."""
        params = {}
        if like:
            params["like"] = like
        if show_limit:
            params["showLimit"] = show_limit
        
        response = await self._client._request(
            "GET", 
            "/api/v2/accounts",
            params=params,
        )
        response.raise_for_status()
        data = response.json()
        if isinstance(data, list):
            return [SnowflakeAccount(**acc) for acc in data]
        return [SnowflakeAccount(**acc) for acc in data.get("accounts", [])]
    
    async def get_account(self, name: str) -> SnowflakeAccount:
        """Get a specific account by name."""
        response = await self._client._request(
            "GET", 
            f"/api/v2/accounts/{name}",
        )
        response.raise_for_status()
        data = response.json()
        return SnowflakeAccount(**data)
