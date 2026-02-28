from pydantic import EmailStr, Field
from typing import Optional
from async_snowflake.data_structures.models.base import SnowflakeResourceModel

class SnowflakeUser(SnowflakeResourceModel):
    
    password: Optional[str] = Field(None, repr=False)  # sensitive field
    login_name: Optional[str] = None
    display_name: Optional[str] = None
    first_name: Optional[str] = None
    middle_name: Optional[str] = None
    last_name: Optional[str] = None
    email: Optional[EmailStr] = None
    must_change_password: Optional[bool] = None
    disabled: Optional[bool] = None
    days_to_expiry: Optional[int] = None
    mins_to_unlock: Optional[int] = None
    default_warehouse: Optional[str] = None
    default_namespace: Optional[str] = None
    default_role: Optional[str] = None
    default_secondary_roles: Optional[str] = Field("ALL", regex=r"^(ALL|NONE)$")
    mins_to_bypass_mfa: Optional[int] = None
    rsa_public_key: Optional[str] = None
    rsa_public_key_2: Optional[str] = None
    comment: Optional[str] = None
    type: Optional[str] = Field(None, regex=r"^(PERSON|SERVICE|LEGACY_SERVICE)$")
    enable_unredacted_query_syntax_error: Optional[bool] = None
    network_policy: Optional[str] = None

    # Read-only fields
    created_on: Optional[str] = None
    last_successful_login: Optional[str] = None
    expires_at: Optional[str] = None
    locked_until: Optional[str] = None
    has_password: Optional[bool] = None
    has_rsa_public_key: Optional[bool] = None
    rsa_public_key_fp: Optional[str] = None
    rsa_public_key_2_fp: Optional[str] = None
    ext_authn_duo: Optional[bool] = None
    ext_authn_uid: Optional[str] = None
    owner: Optional[str] = None
    snowflake_lock: Optional[bool] = None
    snowflake_support: Optional[bool] = None
    mins_to_bypass_network_policy: Optional[int] = None
    password_last_set: Optional[str] = None
    custom_landing_page_url: Optional[str] = None
    custom_landing_page_url_flush_next_ui_load: Optional[bool] = None