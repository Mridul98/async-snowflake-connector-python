from pydantic import Field
from typing import Optional, List, Literal, Union, Annotated
from datetime import datetime
from async_snowflake.data_structures.models.base import SnowflakeResourceModel


class FunctionArgument(SnowflakeResourceModel):
    datatype: str = "TEXT"


class BaseFunction(SnowflakeResourceModel):
    function_type: str


class ServiceFunction(SnowflakeResourceModel):
    function_type: Literal["service-function"] = "service-function"

    # ---------- Required ----------
    arguments: List[FunctionArgument]

    # ---------- Optional ----------
    returns: str = "TEXT"
    max_batch_rows: Optional[int] = Field(None, ge=1)

    language: Optional[str] = None
    body: Optional[str] = None
    signature: Optional[str] = None

    # ---------- Readonly ----------
    created_on: Optional[datetime] = Field(None, frozen=True)


FunctionModel = Annotated[Union[ServiceFunction], Field(discriminator="function_type")]
