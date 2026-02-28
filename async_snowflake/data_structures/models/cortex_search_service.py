from datetime import datetime
from enum import Enum
from typing import List, Optional, Literal, Union
from pydantic import BaseModel, Field
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType

class IndexState(str, Enum):
    ACTIVE = "ACTIVE"
    SUSPENDED = "SUSPENDED"
    INITIALIZING = "INITIALIZING"

class TargetLagBase(BaseModel):
    type: str

class UserDefinedLag(TargetLagBase):
    type: Literal["USER_DEFINED"]
    lag_seconds: int

class DownstreamLag(TargetLagBase):
    type: Literal["DOWNSTREAM"]


TargetLag = Union[UserDefinedLag, DownstreamLag]

class CortexSearchService(SnowflakeResourceModel):
    
    search_column: str
    warehouse: IdentifierType
    definition: str

    target_lag: TargetLag = Field(
        ...,
        discriminator="type"
    )

    columns: Optional[List[str]] = None
    attribute_columns: Optional[List[str]] = None
    comment: Optional[str] = None

    # ---------- Read-only ----------

    created_on: Optional[datetime] = Field(default=None, frozen=True)

    database_name: Optional[str] = Field(default=None, frozen=True)
    schema_name: Optional[str] = Field(default=None, frozen=True)

    source_data_num_rows: Optional[int] = Field(default=None, frozen=True)

    data_timestamp: Optional[datetime] = Field(default=None, frozen=True)

    indexing_state: Optional[IndexState] = Field(default=None)
    serving_state: Optional[IndexState] = Field(default=None)

    indexing_error: Optional[str] = Field(default=None, frozen=True)
    serving_data_bytes: Optional[int] = Field(default=None, frozen=True)
