from pydantic import BaseModel
from typing import Literal, Union, Optional

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

