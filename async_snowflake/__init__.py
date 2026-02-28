"""Async Snowflake Connector for Python.

A lightweight async connector for Snowflake using JWT authentication.
"""

from .authentication import SnowflakeJWTAuthClient, CredentialsManager, SnowflakeCredentials
from .endpoints import SnowflakeClient

__version__ = "0.1.0"
__author__ = "Snowflake Connector Team"

__all__ = [
    "SnowflakeClient",
    "SnowflakeJWTAuthClient",
    "CredentialsManager",
    "SnowflakeCredentials",
]
