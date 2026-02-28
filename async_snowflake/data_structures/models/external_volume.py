from pydantic import Field
from typing import Optional, List, Literal, Union, Annotated
from datetime import datetime
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType

# =========================================================
# Encryption
# =========================================================


class Encryption(SnowflakeResourceModel):
    type: Literal["NONE", "AWS_SSE_S3", "AWS_SSE_KMS", "GCS_SSE_KMS"]

    kms_key_id: Optional[str] = None


# =========================================================
# Storage Providers
# =========================================================


class BaseStorageLocation(SnowflakeResourceModel):
    name: str
    storage_provider: str
    storage_base_url: str
    encryption: Encryption


# ---------- S3 Storage ----------


class StorageLocationS3(BaseStorageLocation):
    storage_provider: Literal["StorageLocationS3"]

    storage_aws_role_arn: Optional[str] = None
    storage_aws_external_id: Optional[str] = None


StorageLocation = Annotated[
    Union[StorageLocationS3], Field(discriminator="storage_provider")
]


# =========================================================
# External Volume
# =========================================================


class ExternalVolume(SnowflakeResourceModel):
    # ---------- Required ----------
    storage_locations: List[StorageLocation]

    # ---------- Optional Writable ----------
    allow_writes: Optional[bool] = None
    comment: Optional[str] = None

    # ---------- Readonly ----------
    created_on: Optional[datetime] = Field(None, frozen=True)

    owner: Optional[IdentifierType] = Field(None, frozen=True)
    owner_role_type: Optional[IdentifierType] = Field(None, frozen=True)
