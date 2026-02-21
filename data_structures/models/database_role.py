from pydantic import BaseModel, Field, ConfigDict, constr
from typing import Optional
from datetime import datetime
from data_structures.types.database_role_types import DatabaseRoleIdentifier

class DatabaseRole(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # -------- Required --------
    name: DatabaseRoleIdentifier = Field(..., description="Name of the database role")

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

    owner: Optional[DatabaseRoleIdentifier] = Field(
        None,
        frozen=True,
        description="Owning role"
    )

    owner_role_type: Optional[DatabaseRoleIdentifier] = Field(
        None,
        frozen=True,
        description="Type of owning role"
    )