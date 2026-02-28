from pydantic import Field
from typing import Optional
from datetime import datetime
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType


class ImageRepository(SnowflakeResourceModel):
    # readonly metadata
    database_name: Optional[str] = Field(default=None, pattern=IdentifierType)
    schema_name: Optional[str] = Field(default=None, pattern=IdentifierType)

    created_on: Optional[datetime] = None
    repository_url: Optional[str] = None
    owner: Optional[str] = None
    owner_role_type: Optional[str] = None
