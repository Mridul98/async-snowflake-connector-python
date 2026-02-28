"""Unit tests for JWT Token authentication and expiration."""
import pytest
import asyncio
from datetime import datetime, timezone, timedelta
from unittest.mock import AsyncMock, MagicMock, patch

from async_snowflake import SnowflakeJWTAuthClient


class TestJWTTokenExpiration:
    """Tests for JWT token expiration and refresh."""

    @pytest.mark.asyncio
    async def test_token_expiration_triggers_refresh(self):
        """Test that expired token triggers automatic refresh."""
        with patch('async_snowflake.authentication.auth_clients.SnowflakeJWTAuthClient._generate_token') as mock_generate:
            mock_generate.return_value = "new_token"
            
            client = SnowflakeJWTAuthClient(
                account="TEST_ACCOUNT",
                user="TEST_USER",
                private_key_path="/home/granite/async-snowflake-connector-python/rsa_key.p8",
            )
            
            await client.initialize()
            
            # Set token as expired (past renew_time)
            client.token = "expired_token"
            client.renew_time = datetime.now(timezone.utc) - timedelta(seconds=10)
            
            # Get token should trigger refresh
            token = await client.get_token()
            
            # Verify new token was generated
            mock_generate.assert_called_once()
            assert token == "new_token"
            
            await client.close()

    @pytest.mark.asyncio
    async def test_token_not_refreshed_if_valid(self):
        """Test that valid token is not refreshed."""
        with patch('async_snowflake.authentication.auth_clients.SnowflakeJWTAuthClient._generate_token') as mock_generate:
            mock_generate.return_value = "new_token"
            
            client = SnowflakeJWTAuthClient(
                account="TEST_ACCOUNT",
                user="TEST_USER",
                private_key_path="/home/granite/async-snowflake-connector-python/rsa_key.p8",
            )
            
            await client.initialize()
            
            # Set token as valid (future renew_time)
            client.token = "valid_token"
            client.renew_time = datetime.now(timezone.utc) + timedelta(minutes=10)
            
            # Get token should NOT trigger refresh
            token = await client.get_token()
            
            # Verify no new token was generated
            mock_generate.assert_not_called()
            assert token == "valid_token"
            
            await client.close()

    @pytest.mark.asyncio
    async def test_token_refresh_before_expiration(self):
        """Test that token is refreshed before it expires (within refresh window)."""
        with patch('async_snowflake.authentication.auth_clients.SnowflakeJWTAuthClient._generate_token') as mock_generate:
            mock_generate.return_value = "refreshed_token"
            
            client = SnowflakeJWTAuthClient(
                account="TEST_ACCOUNT",
                user="TEST_USER",
                private_key_path="/home/granite/async-snowflake-connector-python/rsa_key.p8",
            )
            
            await client.initialize()
            
            # Set refresh time to be very soon
            client.renew_time = datetime.now(timezone.utc) + timedelta(seconds=1)
            
            # Get token should trigger refresh because renew_time is near
            token = await client.get_token()
            
            # Verify new token was generated
            mock_generate.assert_called_once()
            assert token == "refreshed_token"
            
            await client.close()

    @pytest.mark.asyncio
    async def test_concurrent_token_requests_only_generate_once(self):
        """Test that concurrent requests don't trigger multiple token generations."""
        # Track calls to the actual generate method
        call_tracker = {"count": 0, "lock": asyncio.Lock()}
        
        original_generate = SnowflakeJWTAuthClient._generate_token
        
        async def tracked_generate(self):
            async with call_tracker["lock"]:
                call_tracker["count"] += 1
                current_count = call_tracker["count"]
            
            # Simulate slow token generation
            await asyncio.sleep(0.2)
            
            # Call original to properly set token and renew_time
            result = await original_generate(self)
            
            async with call_tracker["lock"]:
                print(f"Generate called, total count: {call_tracker['count']}")
            
            return result
        
        client = SnowflakeJWTAuthClient(
            account="TEST_ACCOUNT",
            user="TEST_USER",
            private_key_path="/home/granite/async-snowflake-connector-python/rsa_key.p8",
        )
        
        await client.initialize()
        
        # Set token as expired to force refresh
        client.token = "expired_token"
        client.renew_time = datetime.now(timezone.utc) - timedelta(seconds=10)
        
        # Patch the method
        with patch.object(SnowflakeJWTAuthClient, '_generate_token', tracked_generate):
            # Make concurrent requests
            results = await asyncio.gather(
                client.get_token(),
                client.get_token(),
                client.get_token(),
            )
        
        # Should only generate token once despite 3 concurrent requests
        # The asyncio.Lock in get_token ensures only one generation happens
        assert call_tracker["count"] == 1, f"Expected 1 call, got {call_tracker['count']}"
        assert all(token == results[0] for token in results)
        
        await client.close()

    @pytest.mark.asyncio
    async def test_token_close_cancels_refresh_task(self):
        """Test that closing client cancels the background refresh task."""
        client = SnowflakeJWTAuthClient(
            account="TEST_ACCOUNT",
            user="TEST_USER",
            private_key_path="/home/granite/async-snowflake-connector-python/rsa_key.p8",
        )
        
        await client.initialize()
        
        # Verify refresh task is running
        assert client._refresh_task is not None
        assert not client._refresh_task.done()
        
        # Close the client
        await client.close()
        
        # Give time for task to finish cancellation
        await asyncio.sleep(0.1)
        
        # Verify refresh task is cancelled/done
        assert client._refresh_task.done() or client._refresh_task.cancelled()
