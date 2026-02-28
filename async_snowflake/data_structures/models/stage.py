from pydantic import BaseModel, SecretStr
from typing import Optional, Literal
from datetime import datetime
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType


class AwsCredentials(BaseModel):
    credential_type: Literal["AwsCredentials"]
    aws_key_id: Optional[SecretStr] = None
    aws_secret_key: Optional[SecretStr] = None
    aws_token: Optional[SecretStr] = None
    aws_role: Optional[str] = None


class StageEncryption(BaseModel):
    type: Literal[
        "SNOWFLAKE_FULL",
        "SNOWFLAKE_SSE",
        "AWS_CSE",
        "AWS_SSE_S3",
        "AWS_SSE_KMS",
        "GCS_SSE_KMS",
        "AZURE_CSE",
        "NONE",
    ]
    master_key: Optional[SecretStr] = None
    kms_key_id: Optional[str] = None


class StageDirectoryTable(BaseModel):
    enable: Optional[bool] = None
    refresh_on_create: Optional[bool] = None
    auto_refresh: Optional[bool] = None
    notification_integration: Optional[str] = None


class Stage(SnowflakeResourceModel):
    kind: Optional[Literal["PERMANENT", "TEMPORARY"]] = "PERMANENT"
    url: Optional[str] = None
    endpoint: Optional[str] = None
    storage_integration: Optional[IdentifierType] = None
    comment: Optional[str] = None
    credentials: Optional[AwsCredentials] = None
    encryption: Optional[StageEncryption] = None
    directory_table: Optional[StageDirectoryTable] = None
    created_on: Optional[datetime] = None
    has_credentials: Optional[bool] = None
    has_encryption_key: Optional[bool] = None
    owner: Optional[IdentifierType] = None
    owner_role_type: Optional[str] = None
    region: Optional[str] = None
    cloud: Optional[str] = None
