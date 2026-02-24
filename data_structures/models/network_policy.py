from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType


class NetworkPolicyBase(SnowflakeResourceModel):

    allowed_network_rule_list: Optional[List[str]] = None
    blocked_network_rule_list: Optional[List[str]] = None
    allowed_ip_list: Optional[List[str]] = None
    blocked_ip_list: Optional[List[str]] = None

    comment: Optional[str] = None


class NetworkPolicyCreate(NetworkPolicyBase):
    pass


class NetworkPolicyRead(NetworkPolicyBase):
    created_on: Optional[datetime] = None
    owner: Optional[str] = Field(default=None, pattern=IdentifierType)
    owner_role_type: Optional[str] = Field(default=None, pattern=IdentifierType)