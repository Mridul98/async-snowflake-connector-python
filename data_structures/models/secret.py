from pydantic import BaseModel, Field, constr
from typing import Optional
from datetime import datetime
from data_structures.types.snowflake_types import IdentifierType
from data_structures.models.base import SnowflakeResourceModel


class PasswordSecretBase(SnowflakeResourceModel):

    type: str = Field("PasswordSecret", const=True)
    comment: Optional[str] = None
    username: Optional[str] = None
    password: Optional[str] = None


class PasswordSecretRead(PasswordSecretBase):
    
    created_on: Optional[datetime] = None
    database_name: Optional[IdentifierType] = None
    schema_name: Optional[IdentifierType] = None
    owner: Optional[IdentifierType] = None
    owner_role_type: Optional[str] = None