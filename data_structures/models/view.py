from pydantic import BaseModel
from typing import List, Optional
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType

class ViewColumn(BaseModel):
    name: IdentifierType
    comment: Optional[str] = None
    datatype: Optional[str] = None  # readonly

class SnowflakeView(SnowflakeResourceModel):
    
    secure: Optional[bool] = None
    kind: Optional[str] = "PERMANENT"  # default PERMANENT
    recursive: Optional[bool] = None
    columns: List[ViewColumn]
    comment: Optional[str] = None
    query: str
    created_on: Optional[str] = None  # readonly, date-time
    database_name: Optional[str] = None  # readonly
    schema_name: Optional[str] = None  # readonly
    owner: Optional[str] = None  # readonly
    owner_role_type: Optional[str] = None  # readonly