from pydantic import BaseModel, constr, Field
from typing import List, Optional, Dict, Any, Literal
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType


class CronSchedule(BaseModel):
    schedule_type: Literal["CronSchedule"] = "CronSchedule"
    cron_expr: str
    timezone: Optional[str] = None


class TaskTargetCompletionInterval(BaseModel):
    schedule_type: Literal["CronSchedule"] = "CronSchedule"
    cron_expr: str
    timezone: Optional[str] = None


class SnowflakeTask(SnowflakeResourceModel):
   
    definition: str
    warehouse: Optional[IdentifierType] = None
    schedule: Optional[CronSchedule] = None
    comment: Optional[str] = None
    finalize: Optional[str] = None
    task_auto_retry_attempts: Optional[int] = None
    config: Optional[Dict[str, Any]] = None
    session_parameters: Optional[Dict[str, Any]] = None
    predecessors: Optional[List[str]] = []
    user_task_managed_initial_warehouse_size: Optional[str] = None
    target_completion_interval: TaskTargetCompletionInterval
    serverless_task_min_statement_size: Optional[str] = None
    serverless_task_max_statement_size: Optional[str] = None
    user_task_timeout_ms: Optional[int] = None
    suspend_task_after_num_failures: Optional[int] = None
    condition: Optional[str] = None
    allow_overlapping_execution: Optional[bool] = None
    error_integration: Optional[str] = None

    # Read-only Snowflake-managed fields
    created_on: Optional[str] = None
    id: Optional[str] = None
    owner: Optional[IdentifierType] = None
    owner_role_type: Optional[str] = None
    state: Optional[str] = None
    last_committed_on: Optional[str] = None
    last_suspended_on: Optional[str] = None
    database_name: Optional[IdentifierType] = None
    schema_name: Optional[IdentifierType] = None