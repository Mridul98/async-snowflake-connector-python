from pydantic import BaseModel, ConfigDict
from data_structures.types.snowflake_types import IdentifierType

class SnowflakeResourceModel(BaseModel):
    name: IdentifierType
    model_config = ConfigDict(
        extra="forbid",
        validate_assignment=True
    )