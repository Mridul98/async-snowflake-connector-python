from datetime import datetime
from enum import Enum
from typing import Optional, Annotated
from pydantic import Field
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType

class ComputePoolState(str, Enum):
    UNKNOWN = "UNKNOWN"
    STARTING = "STARTING"
    IDLE = "IDLE"
    ACTIVE = "ACTIVE"
    STOPPING = "STOPPING"
    SUSPENDED = "SUSPENDED"
    RESIZING = "RESIZING"

class ComputePool(SnowflakeResourceModel):
    
    min_nodes: Annotated[int, Field(strict=True, ge=0)]
    max_nodes: Annotated[int,Field(strict=True, ge=0)]

    instance_family: str

    # ---------- Optional ----------

    auto_resume: Optional[bool] = None
    comment: Optional[str] = None
    auto_suspend_secs: Optional[int] = None

    # ---------- Read-only ----------

    state: Optional[ComputePoolState] = Field(default=None, frozen=True)

    num_services: Optional[int] = Field(default=None, frozen=True)
    num_jobs: Optional[int] = Field(default=None, frozen=True)

    active_nodes: Optional[int] = Field(default=None, frozen=True)
    idle_nodes: Optional[int] = Field(default=None, frozen=True)
    target_nodes: Optional[int] = Field(default=None, frozen=True)

    created_on: Optional[datetime] = Field(default=None, frozen=True)
    resumed_on: Optional[datetime] = Field(default=None, frozen=True)
    updated_on: Optional[datetime] = Field(default=None, frozen=True)

    owner: Optional[str] = Field(default=None, frozen=True)

    is_exclusive: Optional[bool] = Field(default=None, frozen=True)
    application: Optional[str] = Field(default=None, frozen=True)
    budget: Optional[str] = Field(default=None, frozen=True)

    error_code: Optional[str] = Field(default=None, frozen=True)
    status_message: Optional[str] = Field(default=None, frozen=True)

    desired_nodes: Optional[int] = Field(default=None, frozen=True)
    desired_nodes_expire_after: Optional[datetime] = Field(default=None, frozen=True)

    optimize_for_capacity: Optional[bool] = Field(default=None, frozen=True)
    placement_group: Optional[str] = Field(default=None, frozen=True)
