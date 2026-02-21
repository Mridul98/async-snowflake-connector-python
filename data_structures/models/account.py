from pydantic import BaseModel, Field, EmailStr, ConfigDict
from typing import Optional, Literal
from datetime import datetime
from data_structures.types.account_types import AccountName, AccountEdition


class SnowflakeAccount(BaseModel):
    model_config = ConfigDict(extra="forbid")

    organization_name: Optional[str] = Field(
        None, description="Name of the organization.", frozen=True
    )

    name: AccountName = Field(
        ..., description="User-defined account name."
    )

    region_group: Optional[str] = Field(
        None, description="Region group where account is located."
    )

    region: Optional[str] = Field(
        None, description="Snowflake region of the account."
    )

    edition: AccountEdition = Field(
        ..., description="Snowflake Edition of the account."
    )

    created_on: Optional[datetime] = Field(
        None, description="Account creation time.", frozen=True
    )

    account_url: Optional[str] = Field(None, frozen=True)
    account_locator: Optional[str] = Field(None, frozen=True)
    account_locator_url: Optional[str] = Field(None, frozen=True)

    managed_accounts: Optional[int] = Field(None, frozen=True)

    consumption_billing_entity_name: Optional[str] = Field(None, frozen=True)
    marketplace_consumer_billing_entity_name: Optional[str] = Field(None, frozen=True)
    marketplace_provider_billing_entity_name: Optional[str] = Field(None, frozen=True)

    old_account_url: Optional[str] = Field(None, frozen=True)

    comment: Optional[str] = None

    is_org_admin: Optional[bool] = Field(None, frozen=True)

    retention_time: Optional[int] = Field(None, frozen=True)

    dropped_on: Optional[datetime] = Field(None, frozen=True)
    scheduled_deletion_time: Optional[datetime] = Field(None, frozen=True)
    restored_on: Optional[datetime] = Field(None, frozen=True)

    account_old_url_saved_on: Optional[datetime] = Field(None, frozen=True)
    account_old_url_last_used: Optional[datetime] = Field(None, frozen=True)

    organization_old_url: Optional[str] = Field(None, frozen=True)
    organization_old_url_saved_on: Optional[datetime] = Field(None, frozen=True)
    organization_old_url_last_used: Optional[datetime] = Field(None, frozen=True)
    organization_URL_expiration_on: Optional[datetime] = Field(None, frozen=True)

    moved_on: Optional[datetime] = Field(None, frozen=True)

    is_events_account: Optional[bool] = Field(None, frozen=True)

    moved_to_organization: Optional[str] = Field(None, frozen=True)

    admin_name: Optional[str] = Field(
        ..., description="Account administrator name."
    )

    admin_password: Optional[str] = Field(
        None, description="Admin password."
    )

    admin_rsa_public_key: Optional[str] = Field(
        None, description="Admin RSA public key."
    )

    admin_user_type: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None

    email: Optional[EmailStr] = Field(
        ..., description="Admin email."
    )

    must_change_password: Optional[bool] = None

    polaris: Optional[bool] = None
