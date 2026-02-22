from datetime import datetime
from enum import Enum
from typing import List, Optional, Literal
from pydantic import BaseModel, Field
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType

class ApiProvider(str, Enum):
    AWS_API_GATEWAY = "AWS_API_GATEWAY"
    AWS_PRIVATE_API_GATEWAY = "AWS_PRIVATE_API_GATEWAY"
    AWS_GOV_API_GATEWAY = "AWS_GOV_API_GATEWAY"
    AWS_GOV_PRIVATE_API_GATEWAY = "AWS_GOV_PRIVATE_API_GATEWAY"

class ApiHook(BaseModel):
    type: str

class AwsHook(ApiHook):
    type: Literal["AwsHook"]

    api_provider: Optional[ApiProvider] = None
    api_aws_role_arn: Optional[str] = None
    api_key: Optional[str] = None

    api_allowed_prefixes: List[str]
    api_blocked_prefixes: Optional[List[str]] = None

class ApiIntegration(SnowflakeResourceModel):

    api_hook: AwsHook = Field(
        ...,
        discriminator="type"
    )

    enabled: bool

    comment: Optional[str] = None

    created_on: Optional[datetime] = Field(
        default=None,
        description="Read-only creation timestamp"
    )