from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType


class PasswordPolicyBase(SnowflakeResourceModel):

    comment: Optional[str] = None

    password_min_length: Optional[int] = None
    password_max_length: Optional[int] = None
    password_min_upper_case_chars: Optional[int] = None
    password_min_lower_case_chars: Optional[int] = None
    password_min_numeric_chars: Optional[int] = None
    password_min_special_chars: Optional[int] = None

    password_min_age_days: Optional[int] = None
    password_max_age_days: Optional[int] = None

    password_max_retries: Optional[int] = None
    password_lockout_time_mins: Optional[int] = None

    password_history: Optional[int] = None


class PasswordPolicyCreate(PasswordPolicyBase):
    pass


class PasswordPolicyRead(PasswordPolicyBase):
    created_on: Optional[datetime] = None

    database_name: Optional[str] = Field(default=None, pattern=IdentifierType)
    schema_name: Optional[str] = Field(default=None, pattern=IdentifierType)

    owner: Optional[str] = Field(default=None, pattern=IdentifierType)
    owner_role_type: Optional[str] = None