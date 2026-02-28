from pydantic import BaseModel
from typing import List, Optional
from async_snowflake.data_structures.models.base import SnowflakeResourceModel
from async_snowflake.data_structures.types.snowflake_types import IdentifierType


# Version details for Streamlit
class StreamlitVersionDetails(BaseModel):
    name: str
    alias: str
    location_url: str
    source_location_uri: str
    git_commit_hash: str


# Main Streamlit app object
class StreamlitApp(SnowflakeResourceModel):
    comment: Optional[str] = None
    imports: Optional[List[str]] = []
    external_access_integrations: Optional[List[str]] = []
    title: Optional[str] = None
    main_file: Optional[str] = None
    query_warehouse: Optional[str] = None
    default_version: Optional[str] = None  # "first", "last", or "version$N"
    source_location: Optional[str] = None

    # Read-only fields
    created_on: Optional[str] = None
    default_version_details: Optional[StreamlitVersionDetails] = None
    last_version_details: Optional[StreamlitVersionDetails] = None
    database_name: Optional[IdentifierType] = None
    schema_name: Optional[IdentifierType] = None
    owner: Optional[str] = None
    owner_role_type: Optional[str] = None
    url_id: Optional[str] = None
    default_packages: Optional[List[str]] = []
    user_packages: Optional[List[str]] = []
    external_access_secrets: Optional[List[str]] = []
    live_version_location_uri: Optional[str] = None
