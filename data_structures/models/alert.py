from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Literal, Union
from datetime import datetime
from data_structures.types.alert_types import Schedule


class Alert(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str = Field(..., description="Name of the alert")

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