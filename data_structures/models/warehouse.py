from pydantic import Field
from typing import Annotated, Optional
from data_structures.models.base import SnowflakeResourceModel


IntegerType = Annotated[int,Field(ge=0)]

class SnowflakeWarehouse(SnowflakeResourceModel):
    
    warehouse_type: Optional[str] = None  # STANDARD, SNOWPARK-OPTIMIZED
    warehouse_size: Optional[str] = None  # XSMALL, SMALL, MEDIUM, LARGE, XLARGE, XXLARGE, XXXLARGE, X4LARGE, X5LARGE, X6LARGE
    wait_for_completion: Optional[str] = None  # "true" or "false"
    max_cluster_count: Optional[IntegerType] = None
    min_cluster_count: Optional[IntegerType] = None
    scaling_policy: Optional[str] = None  # STANDARD, ECONOMY
    auto_suspend: Optional[IntegerType] = None  # seconds
    auto_resume: Optional[str] = None  # "true" or "false"
    initially_suspended: Optional[str] = None  # "true" or "false"
    resource_monitor: Optional[str] = None
    comment: Optional[str] = None
    enable_query_acceleration: Optional[str] = None  # "true" or "false"
    query_acceleration_max_scale_factor: Optional[IntegerType] = None
    max_concurrency_level: Optional[IntegerType] = None
    statement_queued_timeout_in_seconds: Optional[IntegerType] = None
    statement_timeout_in_seconds: Optional[IntegerType] = None
    target_statement_size: Optional[str] = None  # X-Small, Small, Medium, etc.
    
    # Readonly fields
    state: Optional[str] = None  # STARTED, STARTING, DYNAMIC, etc.
    started_clusters: Optional[IntegerType] = None
    running: Optional[IntegerType] = None
    queued: Optional[IntegerType] = None
    is_default: Optional[bool] = None
    is_current: Optional[bool] = None
    available: Optional[str] = None  # Percentage
    provisioning: Optional[str] = None  # Percentage
    quiescing: Optional[str] = None  # Percentage
    other: Optional[str] = None  # Percentage
    created_on: Optional[str] = None  # date-time
    resumed_on: Optional[str] = None  # date-time
    updated_on: Optional[str] = None  # date-time
    owner: Optional[str] = None
    budget: Optional[str] = None
    owner_role_type: Optional[str] = None
    warehouse_credit_limit: Optional[int] = None  # int64