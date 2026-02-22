from pydantic import BaseModel, Field, ConfigDict
from typing import Optional
from datetime import datetime
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType

class DatabaseRole(SnowflakeResourceModel):

    # -------- Optional Writable --------
    comment: Optional[str] = Field(
        None,
        description="User comment associated to the role"
    )

    # -------- Readonly --------
    created_on: Optional[datetime] = Field(
        None,
        frozen=True,
        description="Creation timestamp"
    )

    granted_to_roles: Optional[int] = Field(
        None,
        ge=0,
        frozen=True
    )

    granted_to_database_roles: Optional[int] = Field(
        None,
        ge=0,
        frozen=True
    )

    granted_database_roles: Optional[int] = Field(
        None,
        ge=0,
        frozen=True
    )

    owner: Optional[IdentifierType] = Field(
        None,
        frozen=True,
        description="Owning role"
    )

    owner_role_type: Optional[IdentifierType] = Field(
        None,
        frozen=True,
        description="Type of owning role"
    )