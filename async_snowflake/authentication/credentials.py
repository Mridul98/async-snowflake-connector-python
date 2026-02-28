"""Credentials management for Snowflake client."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional
from dataclasses import dataclass

try:
    import tomli
except ImportError:
    import toml


@dataclass
class SnowflakeCredentials:
    """Snowflake connection credentials."""

    account: str
    user: str
    private_key_path: str
    region: str = "us-east-1"

    @property
    def base_url(self) -> str:
        """Generate base URL from account and region."""
        return f"https://{self.account}.snowflakecomputing.com"

    def validate(self) -> bool:
        """Validate credentials are set."""
        return bool(self.account and self.user and self.private_key_path)


class CredentialsManager:
    """Manage Snowflake credentials from TOML configuration."""

    DEFAULT_CONFIG_FILE = "credentials.toml"

    def __init__(self, config_path: Optional[str] = None, profile: str = "default"):
        self.config_path = config_path or self._find_config_file()
        self.profile = profile
        self._credentials: Optional[SnowflakeCredentials] = None

    def _find_config_file(self) -> Optional[str]:
        """Find credentials file in standard locations."""
        search_paths = [
            Path.cwd() / self.DEFAULT_CONFIG_FILE,
            Path.home() / ".config" / "async-snowflake" / self.DEFAULT_CONFIG_FILE,
        ]

        for path in search_paths:
            if path.exists():
                return str(path)

        return None

    def load(self) -> SnowflakeCredentials:
        """Load credentials from TOML config."""
        if not self.config_path:
            raise FileNotFoundError(
                f"Credentials file not found. Please create {self.DEFAULT_CONFIG_FILE} "
                "or specify a custom config path."
            )

        try:
            with open(self.config_path, "rb") as f:
                config = tomli.load(f)
        except Exception:
            with open(self.config_path) as f:
                config = toml.load(f)

        if self.profile not in config:
            raise KeyError(
                f"Profile '{self.profile}' not found in credentials file. "
                f"Available profiles: {list(config.keys())}"
            )

        profile_data = config[self.profile]

        account = profile_data.get("account", "")
        user = profile_data.get("user", "")
        private_key_path = profile_data.get("private_key_path", "")

        if not all([account, user, private_key_path]):
            raise ValueError(
                f"Invalid credentials for profile '{self.profile}'. "
                "Please ensure account, user, and private_key_path are set."
            )

        self._credentials = SnowflakeCredentials(
            account=account,
            user=user,
            private_key_path=private_key_path,
            region=profile_data.get("region", "us-east-1"),
        )

        return self._credentials

    @property
    def credentials(self) -> SnowflakeCredentials:
        """Get loaded credentials."""
        if self._credentials is None:
            self._credentials = self.load()
        return self._credentials

    @classmethod
    def from_environment(cls) -> SnowflakeCredentials:
        """Load credentials from environment variables."""
        account = os.environ.get("SNOWFLAKE_ACCOUNT")
        user = os.environ.get("SNOWFLAKE_USER")
        private_key_path = os.environ.get("SNOWFLAKE_PRIVATE_KEY_PATH")
        region = os.environ.get("SNOWFLAKE_REGION", "us-east-1")

        if not all([account, user, private_key_path]):
            raise ValueError(
                "Missing required environment variables: SNOWFLAKE_ACCOUNT, "
                "SNOWFLAKE_USER, SNOWFLAKE_PRIVATE_KEY_PATH"
            )

        return SnowflakeCredentials(
            account=account,
            user=user,
            private_key_path=private_key_path,
            region=region,
        )
