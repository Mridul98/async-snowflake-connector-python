from pydantic import BaseModel
from typing import List, Optional, Literal
from datetime import datetime
from async_snowflake.data_structures.models.base import SnowflakeResourceModel


# ---------- Column ----------
class Column(BaseModel):
    name: str
    datatype: str
    comment: Optional[str] = None
    nullable: Optional[bool] = None
    default_value: Optional[str] = None


# ---------- Constraint ----------
class PrimaryKeyConstraint(BaseModel):
    name: Optional[str] = None
    column_names: List[str]
    constraint_type: Literal["PrimaryKey"]


Constraint = PrimaryKeyConstraint


# ---------- Main Table ----------
class IcebergTable(SnowflakeResourceModel):
    # optional
    comment: Optional[str] = None
    change_tracking: Optional[bool] = None
    max_data_extension_time_in_days: Optional[int] = None
    external_volume: Optional[str] = None
    data_retention_time_in_days: Optional[int] = None
    catalog_sync: Optional[str] = None
    catalog: Optional[str] = None
    storage_serialization_policy: Optional[Literal["COMPATIBLE", "OPTIMIZED"]] = None

    # readonly fields (still allowed in model for responses)
    created_on: Optional[datetime] = None
    database_name: Optional[str] = None
    schema_name: Optional[str] = None
    owner: Optional[str] = None
    owner_role_type: Optional[str] = None
    iceberg_table_type: Optional[str] = None
    can_write_metadata: Optional[str] = None
    auto_refresh: Optional[bool] = None

    # metadata
    catalog_table_name: Optional[str] = None
    catalog_namespace: Optional[str] = None

    # clustering
    cluster_by: Optional[List[str]] = None

    # columns + constraints
    columns: Optional[List[Column]] = None
    constraints: Optional[List[Constraint]] = None

    # storage
    base_location: Optional[str] = None
    replace_invalid_characters: Optional[bool] = None
    metadata_file_path: Optional[str] = None
