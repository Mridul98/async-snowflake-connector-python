from pydantic import BaseModel, Field, constr
from typing import Optional
from datetime import datetime
from async_snowflake.data_structures.types.snowflake_types import IdentifierType
from async_snowflake.data_structures.models.base import SnowflakeResourceModel


class SequenceBase(SnowflakeResourceModel):
  
    start: Optional[int] = None
    increment: Optional[int] = None
    ordered: Optional[bool] = None
    comment: Optional[str] = None
    

class SequenceRead(SequenceBase):
    created_on: Optional[datetime] = None
    database_name: Optional[IdentifierType] = None
    schema_name: Optional[IdentifierType] = None
    owner: Optional[IdentifierType] = None
    owner_role_type: Optional[str] = None