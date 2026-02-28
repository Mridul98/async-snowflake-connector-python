from abc import ABC, abstractmethod
import asyncio
import base64
import hashlib
from typing import NewType
from datetime import datetime, timedelta, timezone

import aiofiles
import jwt as pyjwt
from cryptography.hazmat.primitives.serialization import (
    load_pem_private_key,
    Encoding,
    PublicFormat,
)
from cryptography.hazmat.backends import default_backend


ISSUER = "iss"
EXPIRE_TIME = "exp"
ISSUE_TIME = "iat"
SUBJECT = "sub"

snowflake_auth_token = NewType("snowflake_auth_token", str)


class SnowflakeBaseAuthClient(ABC):
    @abstractmethod
    def get_token(self) -> snowflake_auth_token:
        """Get the current authentication token, generating a new one if necessary.
        This method should check if the current token is still valid (i.e. not expired and not close to expiration).
        If the token is valid, it should return the existing token. If the token is expired or close to expiration, it should generate a new token.
        The method should use an asyncio lock to ensure that only one token generation occurs at a time, preventing multiple concurrent calls from triggering multiple token generations.
        """
        raise NotImplementedError()


class SnowflakeJWTAuthClient(SnowflakeBaseAuthClient):
    ALGORITHM = "RS256"

    def __init__(
        self,
        account: str,
        user: str,
        private_key_path: str,
        lifetime_minutes: int = 59,
        renewal_minutes: int = 54,
        auto_refresh: bool = True,
    ):
        """JWT Authentication client for Snowflake.
        This client generates JWT tokens for Snowflake authentication and can automatically refresh them in the background before they expire.
        The use of


        Args:
            account: Snowflake account identifier (e.g. "myaccount", "myaccount.global", "myaccount-region").
            user: Snowflake username.
            private_key_path: Path to the PEM-encoded RSA private key file.
            lifetime_minutes: Lifetime of the JWT token in minutes (default: 59).
            renewal_minutes: Minutes before expiration to renew the token (default: 54).
            auto_refresh: Whether to automatically refresh the token in the background (default: True).
        """

        self.account = self._normalize_account(account)
        self.user = user.upper()
        self.qualified_username = f"{self.account}.{self.user}"

        self.private_key_path = private_key_path
        self.lifetime = timedelta(minutes=lifetime_minutes)
        self.renewal_delay = timedelta(minutes=renewal_minutes)

        self.private_key = None
        self.token: snowflake_auth_token = None
        self.renew_time = datetime.now(timezone.utc)

        self._lock = asyncio.Lock()
        self._auto_refresh = auto_refresh
        self._refresh_task = None

    # ---------- Initialization ----------

    async def initialize(self):
        """Asynchronously load the private key and start background refresh if enabled.
        Usage:
            client = SnowflakeJWTAuthClient(account, user, private_key_path)
            await client.initialize()
            token = await client.get_token()

        """
        async with aiofiles.open(self.private_key_path, "rb") as f:
            pem = await f.read()

        self.private_key = load_pem_private_key(pem, None, default_backend())

        if self._auto_refresh:
            # offload the background refresh to a separate task to avoid blocking the event loop during initialization
            self._refresh_task = asyncio.create_task(self._background_refresh())

    # ---------- Public API ----------

    async def get_token(self) -> snowflake_auth_token:
        """Get the current JWT token, generating a new one if necessary.
        This method checks if the current token is still valid (i.e. not expired and not close to expiration).
        If the token is valid, it returns the existing token. If the token is expired or close to expiration, it generates a new token.
        The method uses an asyncio lock to ensure that only one token generation occurs at a time,
        preventing multiple concurrent calls from triggering multiple token generations.

        returns: (snowflake_auth_token) The current valid JWT token for Snowflake authentication.
        """
        now = datetime.now(timezone.utc)

        if self.token and now < self.renew_time:
            return self.token

        async with self._lock:
            # double-check after acquiring lock
            now = datetime.now(timezone.utc)
            if self.token and now < self.renew_time:
                return self.token

            return await self._generate_token()

    async def close(self):
        """
        Cancel any background refresh tasks and clean up resources.
        This method should be called when the client is no longer needed to ensure that any background tasks are properly terminated and resources are released.
        Example usage:
            ```python

                    client = SnowflakeJWTAuthClient(account, user, private_key_path)
                    await client.initialize()
                    # use the client to get tokens and interact with Snowflake
                    token = await client.get_token()
                    # when done, close the client to clean up resources
                    await client.close()  # clean up resources when done
        """
        if self._refresh_task:
            self._refresh_task.cancel()

    # ---------- Internals ----------

    async def _generate_token(self) -> snowflake_auth_token:
        """Generate a new JWT token for Snowflake authentication.
        This method creates a new JWT token with the appropriate claims (issuer, subject, issue time, and expiration time) and signs it using the RSA private key.
        The generated token is stored in the instance variable `self.token`, and the next renewal time is calculated based on the current time
        and the specified renewal delay.

        returns: (snowflake_auth_token) The newly generated JWT token for Snowflake authentication.
        """
        now = datetime.now(timezone.utc)
        self.renew_time = now + self.renewal_delay

        payload = {
            ISSUER: f"{self.qualified_username}.{self._fingerprint()}",
            SUBJECT: self.qualified_username,
            ISSUE_TIME: now,
            EXPIRE_TIME: now + self.lifetime,
        }

        # run CPU signing in threadpool
        self.token = await asyncio.to_thread(
            pyjwt.encode,
            payload,
            self.private_key,
            self.ALGORITHM,
        )

        return self.token

    async def _background_refresh(self):
        """Background task that refreshes the JWT token before it expires.
        This method runs in an infinite loop, sleeping until it's time to refresh the token based on the `renew_time`.
        When it's time to refresh, it acquires the lock and generates a new token. If the task is cancelled (e.g. when the client is closed), it exits the loop gracefully.
        """
        while True:
            try:
                sleep_seconds = (
                    self.renew_time - datetime.now(timezone.utc)
                ).total_seconds()
                # ensure we sleep at least 1 second to avoid tight loop if something goes wrong with time calculations
                # this also gives some buffer time for the token to be renewed before it actually expires
                # if the token is already expired or about to expire, we will generate a new one immediately in the next iteration.
                await asyncio.sleep(max(1, sleep_seconds))
                async with self._lock:
                    await self._generate_token()
            except asyncio.CancelledError:
                break

    def _fingerprint(self) -> str:
        """Generate a fingerprint of the public key for the JWT issuer claim.
        The fingerprint is calculated as the SHA-256 hash of the DER-encoded public key, and is prefixed with "SHA256:".
        This method ensures that the issuer claim in the JWT token uniquely identifies the key used for signing,
        which is important for Snowflake to validate the token correctly.

        returns: (str) A string representing the fingerprint of the public key, in the format "SHA256:<base64-encoded-hash>".
        """
        public_bytes = self.private_key.public_key().public_bytes(
            Encoding.DER,
            PublicFormat.SubjectPublicKeyInfo,
        )

        digest = hashlib.sha256(public_bytes).digest()
        return "SHA256:" + base64.b64encode(digest).decode()

    def _normalize_account(self, raw) -> str:
        """Normalize the account identifier by stripping region and global suffixes.
        Snowflake account identifiers can have different formats, such as:
            - myaccount
            - myaccount.global
            - myaccount-region
        This method extracts the base account name by removing any region or global suffixes,
        ensuring consistent handling of the account identifier across different formats.

        returns: (str) The normalized account identifier in uppercase, without any region or global suffixes.
        Example: "myaccount", "myaccount.global", and "myaccount-region" would all be normalized to "MYACCOUNT".
        """
        if ".global" not in raw:
            idx = raw.find(".")
            if idx > 0:
                raw = raw[:idx]
        else:
            idx = raw.find("-")
            if idx > 0:
                raw = raw[:idx]
        return raw.upper()
