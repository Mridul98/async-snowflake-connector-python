from pydantic import BaseModel, Field, constr
from typing import Optional
from datetime import datetime
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType

class RoleBase(SnowflakeResourceModel):
    
    comment: Optional[str] = None


class RoleRead(RoleBase):
    created_on: Optional[datetime] = None
    owner: Optional[IdentifierType] = None
    is_default: Optional[bool] = None
    is_current: Optional[bool] = None
    is_inherited: Optional[bool] = None
    assigned_to_users: Optional[int] = None
    granted_to_roles: Optional[int] = None
    granted_roles: Optional[int] = None