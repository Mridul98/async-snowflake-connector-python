from typing import Optional, Literal
from datetime import datetime
from async_snowflake.data_structures.types.snowflake_types import IdentifierType
from async_snowflake.data_structures.models.base import SnowflakeResourceModel


class PasswordSecretBase(SnowflakeResourceModel):
    type: Literal["PasswordSecret"] = "PasswordSecret"
    comment: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class PasswordSecretRead(PasswordSecretBase):
    created_on: Optional[datetime] = None
    database_name: Optional[IdentifierType] = None
    schema_name: Optional[IdentifierType] = None
    owner: Optional[IdentifierType] = None
    owner_role_type: Optional[str] = None
