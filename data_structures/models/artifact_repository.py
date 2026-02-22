from datetime import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType

class RepositoryType(str, Enum):
    PIP = "PIP"

class ArtifactRepository(SnowflakeResourceModel):

    type: RepositoryType = Field(
        ...,
        description="Repository type (currently only PIP)"
    )

    api_integration: str = Field(
        ...,
        description="Link to an integration object"
    )

    comment: Optional[str] = None

    # ---------- Read-only fields ----------

    created_on: Optional[datetime] = Field(
        default=None,
        description="Creation timestamp",
        frozen=True
    )

    database_name: Optional[IdentifierType] = Field(
        default=None,
        frozen=True
    )

    schema_name: Optional[IdentifierType] = Field(
        default=None,
        frozen=True
    )

    owner: Optional[IdentifierType] = Field(
        default=None,
        frozen=True
    )

    owner_role_type: Optional[IdentifierType] = Field(
        default=None,
        frozen=True
    )