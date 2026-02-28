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
                private_key_path="rsa_key.p8",
            )
            
            with patch.object(client, 'initialize', AsyncMock()):
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
                private_key_path="rsa_key.p8",
            )
            
            with patch.object(client, 'initialize', AsyncMock()):
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
                private_key_path="rsa_key.p8",
            )
            
            with patch.object(client, 'initialize', AsyncMock()):
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
        call_tracker = {"count": 0, "lock": asyncio.Lock()}
        
        async def tracked_generate(self):
            async with call_tracker["lock"]:
                call_tracker["count"] += 1
            
            await asyncio.sleep(0.2)
            
            self.token = "tracked_token"
            self.renew_time = datetime.now(timezone.utc) + timedelta(minutes=10)
            return self.token
        
        client = SnowflakeJWTAuthClient(
            account="TEST_ACCOUNT",
            user="TEST_USER",
            private_key_path="rsa_key.p8",
        )
        
        with patch.object(client, 'initialize', AsyncMock()):
            await client.initialize()
        
        client.token = "expired_token"
        client.renew_time = datetime.now(timezone.utc) - timedelta(seconds=10)
        
        with patch.object(client, '_fingerprint', return_value="SHA256:abc123"):
            with patch.object(SnowflakeJWTAuthClient, '_generate_token', tracked_generate):
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
            private_key_path="rsa_key.p8",
        )
        
        mock_key = MagicMock()
        mock_key.public_key.return_value.public_bytes.return_value = b"mock_public_key_bytes"
        
        mock_file = AsyncMock()
        mock_file.read = AsyncMock(return_value=b"fake_pem_data")
        mock_file.__aenter__ = AsyncMock(return_value=mock_file)
        mock_file.__aexit__ = AsyncMock(return_value=None)
        
        with patch('aiofiles.open', return_value=mock_file):
            with patch('async_snowflake.authentication.auth_clients.load_pem_private_key', return_value=mock_key):
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
