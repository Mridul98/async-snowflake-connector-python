from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List
from datetime import datetime
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType


class EventTableColumn(SnowflakeResourceModel):

    name: Optional[str] = None
    datatype: Optional[str] = None
    nullable: Optional[bool] = None
    default: Optional[str] = None
    primary_key: Optional[bool] = None
    unique_key: Optional[bool] = None
    check: Optional[str] = None
    expression: Optional[str] = None
    comment: Optional[str] = None


# =========================================================
# Main Event Table Model
# =========================================================

class EventTable(SnowflakeResourceModel):

    # ---------- Optional Writable ----------
    cluster_by: Optional[List[str]] = None

    data_retention_time_in_days: Optional[int] = Field(None, ge=0)
    max_data_extension_time_in_days: Optional[int] = Field(None, ge=0)

    change_tracking: Optional[bool] = None

    default_ddl_collation: Optional[str] = None
    comment: Optional[str] = None

    # ---------- Readonly Metadata ----------
    created_on: Optional[datetime] = Field(None, frozen=True)

    database_name: Optional[str] = Field(None, frozen=True)
    schema_name: Optional[str] = Field(None, frozen=True)

    owner: Optional[str] = Field(None, frozen=True)
    owner_role_type: Optional[str] = Field(None, frozen=True)

    rows: Optional[int] = Field(None, ge=0, frozen=True)
    bytes: Optional[int] = Field(None, ge=0, frozen=True)

    automatic_clustering: Optional[bool] = Field(None, frozen=True)

    search_optimization: Optional[bool] = Field(None, frozen=True)

    search_optimization_progress: Optional[int] = Field(
        None,
        ge=0,
        le=100,
        frozen=True
    )

    search_optimization_bytes: Optional[int] = Field(
        None,
        ge=0,
        frozen=True
    )

    columns: Optional[List[EventTableColumn]] = Field(
        None,
        frozen=True
    )