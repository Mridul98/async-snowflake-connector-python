from pydantic import BaseModel, Field, ConfigDict, constr
from typing import Optional, Literal
from datetime import datetime
from data_structures.types.common_types import LogLevel
from data_structures.types.database_types import DatabaseName, DatabaseKind, TraceLevel, Role


class Database(BaseModel):
    model_config = ConfigDict(extra="forbid")

    # ---------- Required ----------
    name: DatabaseName = Field(..., description="Database name")

    # ---------- Optional Writeable ----------
    kind: Optional[DatabaseKind] = Field(
        "PERMANENT",
        description="Database type"
    )

    comment: Optional[str] = None

    data_retention_time_in_days: Optional[int] = None

    default_ddl_collation: Optional[str] = None

    log_level: Optional[LogLevel] = None

    max_data_extension_time_in_days: Optional[int] = None

    suspend_task_after_num_failures: Optional[int] = None

    trace_level: Optional[TraceLevel] = None

    user_task_managed_initial_warehouse_size: Optional[str] = None

    user_task_timeout_ms: Optional[int] = None

    serverless_task_min_statement_size: Optional[str] = None
    serverless_task_max_statement_size: Optional[str] = None

    # ---------- Readonly ----------
    created_on: Optional[datetime] = Field(None, frozen=True)

    is_default: Optional[bool] = Field(None, frozen=True)
    is_current: Optional[bool] = Field(None, frozen=True)

    origin: Optional[str] = Field(None, frozen=True)
    owner: Optional[str] = Field(None, frozen=True)

    options: Optional[str] = Field(None, frozen=True)

    retention_time: Optional[int] = Field(None, frozen=True)

    dropped_on: Optional[datetime] = Field(None, frozen=True)

    budget: Optional[str] = Field(None, frozen=True)

    owner_role_type: Optional[Role] = Field(None, frozen=True)