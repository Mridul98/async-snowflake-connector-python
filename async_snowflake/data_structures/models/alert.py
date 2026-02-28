from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, Union
from datetime import datetime

from async_snowflake.data_structures.models.base import SnowflakeResourceModel

class BaseSchedule(BaseModel):
    schedule_type: str


class CronSchedule(BaseSchedule):
    schedule_type: Literal["CronSchedule"]
    cron_expr: str
    timezone: Optional[str] = None


class MinutesSchedule(BaseSchedule):
    schedule_type: Literal["MinutesSchedule"]
    minutes: int

Schedule = Union[CronSchedule, MinutesSchedule]

class Alert(SnowflakeResourceModel):

    comment: Optional[str] = Field(
        None,
        description="User comment associated to the alert"
    )

    schedule: Schedule = Field(
        ...,
        discriminator="schedule_type",
        description="Execution schedule"
    )

    warehouse: Optional[str] = None

    condition: str = Field(
        ...,
        description="SQL statement evaluated to determine if alert triggers"
    )

    action: str = Field(
        ...,
        description="SQL statement executed when alert triggers"
    )

    # ---------- Readonly Fields ----------

    created_on: Optional[datetime] = Field(None, frozen=True)

    database_name: Optional[str] = Field(None, frozen=True)
    schema_name: Optional[str] = Field(None, frozen=True)

    owner: Optional[str] = Field(None, frozen=True)
    owner_role_type: Optional[str] = Field(None, frozen=True)

    state: Optional[str] = Field(None, frozen=True)