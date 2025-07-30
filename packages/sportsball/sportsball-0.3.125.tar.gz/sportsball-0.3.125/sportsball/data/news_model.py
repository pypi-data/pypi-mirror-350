"""The prototype class for news."""

import datetime

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType


class NewsModel(BaseModel):
    """The serialisable news class."""

    title: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.TEXT})
    published: datetime.datetime
    summary: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.TEXT})
    source: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
