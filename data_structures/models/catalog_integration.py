from datetime import datetime
from enum import Enum
from typing import Optional, Literal, Union
from pydantic import BaseModel, Field
from data_structures.models.base import SnowflakeResourceModel
from data_structures.types.snowflake_types import IdentifierType

class TableFormat(str, Enum):
    ICEBERG = "ICEBERG"


class IntegrationType(str, Enum):
    CATALOG = "CATALOG"


class IntegrationCategory(str, Enum):
    CATALOG = "CATALOG"

class CatalogBase(BaseModel):
    catalog_source: str

class GlueCatalog(CatalogBase):
    catalog_source: Literal["Glue"]

    glue_aws_role_arn: Optional[str] = None
    glue_catalog_id: Optional[str] = None
    glue_region: Optional[str] = None
    catalog_namespace: Optional[str] = None

CatalogType = Union[GlueCatalog]

class CatalogIntegration(SnowflakeResourceModel):

    catalog: CatalogType = Field(
        ...,
        discriminator="catalog_source"
    )

    table_format: TableFormat

    enabled: bool

    comment: Optional[str] = None

    # ---------- Read-only ----------

    type: Optional[IntegrationType] = Field(
        default=None,
        frozen=True
    )

    category: Optional[IntegrationCategory] = Field(
        default=None,
        frozen=True
    )

    created_on: Optional[datetime] = Field(
        default=None,
        frozen=True
    )