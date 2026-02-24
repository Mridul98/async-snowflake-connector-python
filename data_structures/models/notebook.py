from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from data_structures.types.snowflake_types import IdentifierType 
from data_structures.models.base import SnowflakeResourceModel


class NotebookVersionDetails(SnowflakeResourceModel):

    alias: Optional[str] = None
    location_url: Optional[str] = None
    source_location_uri: Optional[str] = None
    git_commit_hash: Optional[str] = None


class NotebookBase(SnowflakeResourceModel):

    version: Optional[str] = None
    fromLocation: Optional[str] = None
    main_file: Optional[str] = None
    comment: Optional[str] = None
    default_version: Optional[str] = None
    query_warehouse: Optional[str] = None
    title: Optional[str] = None

    runtime_name: Optional[str] = None
    compute_pool: Optional[str] = None

    import_urls: Optional[List[str]] = None
    external_access_integrations: Optional[List[str]] = None

    idle_auto_shutdown_time_seconds: Optional[int] = None


class NotebookCreate(NotebookBase):
    pass


class NotebookRead(NotebookBase):

    created_on: Optional[datetime] = None

    database_name: Optional[str] = Field(default=None, pattern=IdentifierType)
    schema_name: Optional[str] = Field(default=None, pattern=IdentifierType)

    owner: Optional[str] = Field(default=None, pattern=IdentifierType)
    owner_role_type: Optional[str] = None

    url_id: Optional[str] = None

    default_packages: Optional[str] = None
    user_packages: Optional[str] = None
    external_access_secrets: Optional[str] = None

    default_version_details: Optional[NotebookVersionDetails] = None
    last_version_details: Optional[NotebookVersionDetails] = None

    live_version_location_uri: Optional[str] = None

    budget: Optional[str] = Field(default=None, pattern=IdentifierType)