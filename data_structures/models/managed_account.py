from pydantic import BaseModel, Field
from typing import Optional, Literal
from datetime import datetime
from data_structures.models.base import SnowflakeResourceModel


class ManagedAccountBase(SnowflakeResourceModel):

    comment: Optional[str] = None
    admin_name: Optional[str] = None
    admin_password: Optional[str] = Field(default=None, description="password")
    account_type: Literal["READER"] = "READER"


class ManagedAccountCreate(ManagedAccountBase):
    pass


class ManagedAccountRead(ManagedAccountBase):
    cloud: Optional[str] = None
    region: Optional[str] = None
    locator: Optional[str] = None
    created_on: Optional[datetime] = None
    url: Optional[str] = None
    account_locator_url: Optional[str] = None