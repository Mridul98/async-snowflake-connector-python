from pydantic import BaseModel, Field, constr
from typing import Optional, List
from datetime import datetime
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType


class ProcedureArgument(SnowflakeResourceModel):

    datatype: str
    default_value: Optional[str] = None
    nullable: Optional[bool] = None


# ---------------------------
# Procedure Return Type
# ---------------------------
class ProcedureReturnType(BaseModel):

    type: IdentifierType # DATATYPE or TABLE
    datatype: Optional[str] = None


# ---------------------------
# Language Configuration
# ---------------------------
class ProcedureLanguageConfig(BaseModel):
    language: IdentifierType  # JAVA, PYTHON, SQL, etc.
    called_on_null_input: Optional[bool] = None
    runtime_version: Optional[str] = None
    packages: Optional[List[str]] = None
    imports: Optional[List[str]] = None
    handler: Optional[str] = None
    external_access_integrations: Optional[List[str]] = None
    secrets: Optional[dict] = None
    target_path: Optional[str] = None


# ---------------------------
# Base Procedure Model
# ---------------------------
class ProcedureBase(SnowflakeResourceModel):

    execute_as: Optional[str] = None  # CALLER or OWNER
    is_secure: Optional[bool] = None
    arguments: List[ProcedureArgument]
    return_type: ProcedureReturnType
    language_config: ProcedureLanguageConfig
    comment: Optional[str] = None
    body: Optional[str] = None


# ---------------------------
# Read Model (with readonly fields)
# ---------------------------
class ProcedureRead(ProcedureBase):
    created_on: Optional[datetime] = None
    schema_name: Optional[str] = Field(default=None, pattern=IdentifierType)
    database_name: Optional[str] = Field(default=None, pattern=IdentifierType)
    min_num_arguments: Optional[int] = None
    max_num_arguments: Optional[int] = None
    owner: Optional[str] = Field(default=None, pattern=IdentifierType)
    owner_role_type: Optional[str] = None
    is_builtin: Optional[bool] = None