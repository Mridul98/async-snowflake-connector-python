from pydantic import BaseModel, constr, Field
from typing import Literal, Optional
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType


class PointOfTimeTimestamp(BaseModel):
    point_of_time_type: Literal["PointOfTimeTimestamp"] = Field(..., alias="point_of_time_type")
    reference: Literal["at", "before"]
    timestamp: Optional[str] = None  # e.g., TO_TIMESTAMP(1749423600)


class StreamSourceTable(BaseModel):
    src_type: Literal["StreamSourceTable"] = Field(..., alias="src_type")
    name: IdentifierType
    database_name: Optional[IdentifierType] = None
    schema_name: Optional[IdentifierType] = None
    append_only: Optional[bool] = False
    show_initial_rows: Optional[bool] = False
    point_of_time: PointOfTimeTimestamp


class Stream(SnowflakeResourceModel):
    name: IdentifierType
    stream_source: StreamSourceTable
    comment: Optional[str] = None

    # Read-only metadata
    created_on: Optional[str] = None
    database_name: Optional[IdentifierType] = None
    schema_name: Optional[IdentifierType] = None
    owner: Optional[str] = None
    table_name: Optional[str] = None
    stale: Optional[bool] = None
    mode: Optional[Literal["APPEND_ONLY", "INSERT_ONLY", "DEFAULT"]] = "DEFAULT"
    stale_after: Optional[str] = None
    invalid_reason: Optional[str] = "N/A"
    owner_role_type: Optional[str] = None
    type: Optional[str] = "DELTA"  # Snowflake currently supports only DELTA streams