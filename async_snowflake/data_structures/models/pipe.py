from pydantic import Field
from typing import Optional
from datetime import datetime
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType, CopyRegexType


class PipeBase(SnowflakeResourceModel):
    
    copy_statement: CopyRegexType
    
    comment: Optional[str] = None
    auto_ingest: Optional[bool] = None
    error_integration: Optional[str] = None
    aws_sns_topic: Optional[str] = None
    integration: Optional[str] = None


class PipeCreate(PipeBase):
    pass


class PipeRead(PipeBase):
    created_on: Optional[datetime] = None
    database_name: Optional[str] = Field(default=None, pattern=IdentifierType)
    schema_name: Optional[str] = Field(default=None, pattern=IdentifierType)
    owner: Optional[str] = Field(default=None, pattern=IdentifierType)
    owner_role_type: Optional[str] = None
    pattern: Optional[str] = None
    invalid_reason: Optional[str] = None
    budget: Optional[str] = None