from pydantic import BaseModel, constr, Field
from typing import List, Optional, Union, Literal
from async_snowflake.data_structures.models.base import SnowflakeResourceModel 
from async_snowflake.data_structures.types.snowflake_types import IdentifierType


class UDFArgumentReturnType(BaseModel):
    type: IdentifierType  # discriminator: ReturnDataType
    datatype: Optional[str] = None
    nullable: Optional[bool] = None


class UDFArgument(SnowflakeResourceModel):
    
    datatype: str
    default_value: Optional[str] = None
    return_type: UDFArgumentReturnType


class JavaLanguageConfig(BaseModel):
    language: Literal["JavaFunction"] = "JavaFunction"
    called_on_null_input: Optional[bool] = None
    runtime_version: Optional[str] = None  # e.g., "11.x" or "17.x"
    packages: Optional[List[str]] = None
    imports: Optional[List[str]] = None
    handler: Optional[str] = None


class SnowflakeUDF(SnowflakeResourceModel):
    
    is_temporary: Optional[bool] = None
    is_aggregate: Optional[bool] = None
    is_memoizable: Optional[bool] = None
    is_table_function: Optional[bool] = None  # readonly
    valid_for_clustering: Optional[bool] = None  # readonly
    is_secure: Optional[bool] = None
    arguments: List[UDFArgument]
    language_config: JavaLanguageConfig
    is_volatile: Optional[bool] = None
    external_access_integrations: Optional[List[str]] = None
    secrets: Optional[dict] = None
    target_path: Optional[str] = None
    comment: Optional[str] = None
    body: Optional[str] = None
    created_on: Optional[str] = None  # readonly
    schema_name: Optional[str] = None  # readonly
    database_name: Optional[str] = None  # readonly
    min_num_arguments: Optional[int] = None  # readonly
    max_num_arguments: Optional[int] = None  # readonly
    owner: Optional[str] = None  # readonly
    owner_role_type: Optional[str] = None  # readonly
    is_builtin: Optional[bool] = None  # readonly