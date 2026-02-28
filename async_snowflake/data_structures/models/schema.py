from typing import Optional
from datetime import datetime
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType


class SchemaBase(SnowflakeResourceModel):
    kind: Optional[str] = "PERMANENT"
    comment: Optional[str] = None
    managed_access: Optional[bool] = False
    data_retention_time_in_days: Optional[int] = None
    default_ddl_collation: Optional[str] = None
    log_level: Optional[str] = None
    pipe_execution_paused: Optional[bool] = None
    max_data_extension_time_in_days: Optional[int] = None
    suspend_task_after_num_failures: Optional[int] = None
    trace_level: Optional[str] = None
    user_task_managed_initial_warehouse_size: Optional[str] = None
    user_task_timeout_ms: Optional[int] = None
    serverless_task_min_statement_size: Optional[str] = None
    serverless_task_max_statement_size: Optional[str] = None


class SchemaRead(SchemaBase):
    created_on: Optional[datetime] = None
    is_default: Optional[bool] = None
    is_current: Optional[bool] = None
    database_name: Optional[IdentifierType] = None
    owner: Optional[IdentifierType] = None
    options: Optional[str] = None
    retention_time: Optional[int] = None
    dropped_on: Optional[datetime] = None
    owner_role_type: Optional[str] = None
    budget: Optional[str] = None
