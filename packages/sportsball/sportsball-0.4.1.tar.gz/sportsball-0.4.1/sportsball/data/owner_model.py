"""The prototype class for an owner."""

from typing import Literal

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType

OWNER_IDENTIFIER_COLUMN: Literal["identifier"] = "identifier"
OWNER_NAME_COLUMN: Literal["name"] = "name"


class OwnerModel(BaseModel):
    """The serialisable owner class."""

    identifier: str = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL},
        alias=OWNER_IDENTIFIER_COLUMN,
    )
    name: str = Field(..., alias=OWNER_NAME_COLUMN)
