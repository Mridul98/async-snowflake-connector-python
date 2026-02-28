from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from async_snowflake.data_structures.models.base import SnowflakeResourceModel


class NotificationEmail(BaseModel):
    type: Literal["NotificationEmail"] = Field(default="NotificationEmail")
    allowed_recipients: Optional[List[str]] = None
    default_recipients: Optional[List[str]] = None
    default_subject: Optional[str] = None


class NotificationIntegrationBase(SnowflakeResourceModel):
  
    enabled: Optional[bool] = None
    comment: Optional[str] = None
    notification_hook: NotificationEmail


class NotificationIntegrationCreate(NotificationIntegrationBase):
    pass


class NotificationIntegrationRead(NotificationIntegrationBase):
    created_on: Optional[datetime] = None