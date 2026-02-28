from pydantic import BaseModel
from typing import Optional, List, Union
from datetime import datetime
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType


class ServiceSpecStageFile(BaseModel):
    spec_type: str = "ServiceSpecStageFile"
    stage: str
    spec_file: str


class ServiceBase(SnowflakeResourceModel):
    compute_pool: str
    auto_resume: Optional[bool] = None
    min_ready_instances: Optional[int] = None
    min_instances: Optional[int] = None
    max_instances: Optional[int] = None
    auto_suspend_secs: Optional[int] = None
    status: Optional[str] = None
    query_warehouse: Optional[IdentifierType] = None
    external_access_integrations: Optional[List[str]] = None
    comment: Optional[str] = None
    spec: Union[ServiceSpecStageFile]  # can be extended for other spec types


class ServiceRead(ServiceBase):
    current_instances: Optional[int] = None
    target_instances: Optional[int] = None
    database_name: Optional[IdentifierType] = None
    schema_name: Optional[IdentifierType] = None
    owner: Optional[IdentifierType] = None
    owner_role_type: Optional[str] = None
    dns_name: Optional[str] = None
    created_on: Optional[datetime] = None
    updated_on: Optional[datetime] = None
    resumed_on: Optional[datetime] = None
    suspended_on: Optional[datetime] = None
    is_job: Optional[bool] = None
    spec_digest: Optional[str] = None
    is_upgrading: Optional[bool] = None
    managing_object_domain: Optional[str] = None
    managing_object_name: Optional[str] = None
    is_async_job: Optional[bool] = None
