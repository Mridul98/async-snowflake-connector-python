from pydantic import BaseModel, Field
from typing import Optional, List, Literal
from datetime import datetime
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType


class NetworkRuleBase(SnowflakeResourceModel):
    type: str
    mode: Optional[Literal["INGRESS", "INTERNAL_STAGE", "EGRESS"]] = None
    value_list: Optional[List[str]] = None
    comment: Optional[str] = None


class NetworkRuleCreate(NetworkRuleBase):
    pass


class NetworkRuleRead(NetworkRuleBase):
    created_on: Optional[datetime] = None

    database_name: Optional[str] = Field(default=None, pattern=IdentifierType)
    schema_name: Optional[str] = Field(default=None, pattern=IdentifierType)

    owner: Optional[str] = Field(default=None, pattern=IdentifierType)
    owner_role_type: Optional[str] = None