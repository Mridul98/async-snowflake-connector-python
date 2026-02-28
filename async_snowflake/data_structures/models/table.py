from pydantic import BaseModel
from typing import List, Optional, Literal
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType


# Column constraints
class PrimaryKeyConstraint(BaseModel):
    name: Optional[str] = None
    column_names: List[str]
    constraint_type: Literal["PrimaryKey"] = "PrimaryKey"
    comment: Optional[str] = None


# Column definition
class TableColumn(BaseModel):
    name: str
    datatype: str
    nullable: bool = True
    collate: Optional[str] = None
    default: Optional[str] = None
    autoincrement: Optional[bool] = False
    autoincrement_start: Optional[int] = None
    autoincrement_increment: Optional[int] = None
    constraints: Optional[List[PrimaryKeyConstraint]] = []
    comment: Optional[str] = None


# Main Table model
class SnowflakeTable(SnowflakeResourceModel):
    kind: Optional[str] = "PERMANENT"  # PERMANENT, TRANSIENT, TEMPORARY
    cluster_by: Optional[List[str]] = []
    enable_schema_evolution: Optional[bool] = False
    change_tracking: Optional[bool] = False
    data_retention_time_in_days: Optional[int] = None
    max_data_extension_time_in_days: Optional[int] = None
    default_ddl_collation: Optional[str] = None
    columns: List[TableColumn] = []
    constraints: Optional[List[PrimaryKeyConstraint]] = []
    comment: Optional[str] = None

    # Read-only fields
    created_on: Optional[str] = None
    database_name: Optional[IdentifierType] = None
    schema_name: Optional[IdentifierType] = None
    rows: Optional[int] = None
    bytes: Optional[int] = None
    owner: Optional[str] = None
    dropped_on: Optional[str] = None
    automatic_clustering: Optional[bool] = None
    search_optimization: Optional[bool] = None
    search_optimization_progress: Optional[int] = None
    search_optimization_bytes: Optional[int] = None
    owner_role_type: Optional[str] = None
    budget: Optional[str] = None
    table_type: Optional[str] = (
        None  # NORMAL, DYNAMIC, EXTERNAL, EVENT, HYBRID, ICEBERG, IMMUTABLE
    )
