from pydantic import BaseModel, constr, Field
from typing import List, Optional
from data_structures.models.base import SnowflakeResourceModel 
from data_structures.types.snowflake_types import IdentifierType

class SnowflakeTag(SnowflakeResourceModel):

    allowed_values: Optional[List[str]] = []
    propagate: Optional[str] = None  # e.g., 'true'/'false' or custom propagation rules
    on_conflict: Optional[str] = None  # behavior when propagated tag conflicts occur
    comment: Optional[str] = None

    # Read-only Snowflake-managed fields
    created_on: Optional[str] = None  # date-time
    database_name: Optional[IdentifierType] = None
    schema_name: Optional[IdentifierType] = None
    owner: Optional[IdentifierType] = None
    owner_role_type: Optional[str] = None