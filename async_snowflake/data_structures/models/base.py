from pydantic import BaseModel, ConfigDict
from async_snowflake.data_structures.types.snowflake_types import IdentifierType

class SnowflakeResourceModel(BaseModel):
    name: IdentifierType
    model_config = ConfigDict(
        extra="allow",
        validate_assignment=True
    )