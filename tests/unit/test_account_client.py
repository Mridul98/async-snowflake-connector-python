"""Unit tests for AccountClient."""
import pytest


class TestAccountClient:
    """Unit tests for AccountClient."""

    @pytest.mark.asyncio
    async def test_lazy_loading(self, mock_client):
        """Test account client is created lazily."""
        from async_snowflake.endpoints.accounts import AccountClient
        account_client = mock_client.account
        assert isinstance(account_client, AccountClient)
