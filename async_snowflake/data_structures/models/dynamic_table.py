from pydantic import BaseModel, Field
from typing import Optional, Literal, List, Union, Annotated
from datetime import datetime
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType

class DynamicColumn(BaseModel):
    name: IdentifierType
    datatype: Optional[str] = None
    comment: Optional[str] = None


class BaseLag(BaseModel):
    type: str


class UserDefinedLag(BaseLag):
    type: Literal["USER_DEFINED"]
    lag: Optional[str] = None


class DownstreamLag(BaseLag):
    type: Literal["DOWNSTREAM"]


TargetLag = Union[UserDefinedLag, DownstreamLag]


class DynamicTable(SnowflakeResourceModel):

    target_lag: TargetLag = Field(..., discriminator="type")
    warehouse: IdentifierType
    query: str

    # ---------- Optional Writable ----------
    kind: Optional[Literal["PERMANENT", "TRANSIENT"]] = "PERMANENT"

    columns: Optional[List[DynamicColumn]] = None

    refresh_mode: Optional[
        Literal["AUTO", "FULL", "INCREMENTAL"]
    ] = None

    initialize: Optional[
        Literal["ON_CREATE", "ON_SCHEDULE"]
    ] = None

    cluster_by: Optional[List[str]] = None

    data_retention_time_in_days: Optional[int] = Field(None, ge=0)
    max_data_extension_time_in_days: Optional[int] = Field(None, ge=0)

    comment: Optional[str] = None

    # ---------- Readonly ----------
    created_on: Optional[datetime] = Field(None, frozen=True)

    database_name: Optional[str] = Field(None, frozen=True)
    schema_name: Optional[str] = Field(None, frozen=True)

    rows: Optional[int] = Field(None, ge=0, frozen=True)
    bytes: Optional[int] = Field(None, ge=0, frozen=True)

    scheduling_state: Optional[
        Literal["RUNNING", "SUSPENDED"]
    ] = Field(None, frozen=True)

    automatic_clustering: Optional[bool] = Field(None, frozen=True)

    owner: Optional[str] = Field(None, frozen=True)
    owner_role_type: Optional[str] = Field(None, frozen=True)

    budget: Optional[str] = Field(None, frozen=True)