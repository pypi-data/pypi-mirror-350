"""The prototype class for a coach."""

import datetime
from typing import Literal

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType

COACH_IDENTIFIER_COLUMN: Literal["identifier"] = "identifier"
COACH_NAME_COLUMN: Literal["name"] = "name"
COACH_BIRTH_DATE_COLUMN: Literal["birth_date"] = "birth_date"
COACH_AGE_COLUMN: Literal["age"] = "age"


class CoachModel(BaseModel):
    """The serialisable coach class."""

    identifier: str = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL},
        alias=COACH_IDENTIFIER_COLUMN,
    )
    name: str = Field(..., alias=COACH_NAME_COLUMN)
    birth_date: datetime.date | None = Field(..., alias=COACH_BIRTH_DATE_COLUMN)
    age: int | None = Field(..., alias=COACH_AGE_COLUMN)
