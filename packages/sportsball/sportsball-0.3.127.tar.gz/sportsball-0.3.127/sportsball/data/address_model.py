"""A class for holding address information."""

from typing import Literal

from pydantic import BaseModel, Field

from .field_type import TYPE_KEY, FieldType
from .weather_model import WeatherModel

ADDRESS_LATITUDE_COLUMN: Literal["latitude"] = "latitude"
ADDRESS_LONGITUDE_COLUMN: Literal["longitude"] = "longitude"
ADDRESS_TIMEZONE_COLUMN: Literal["timezone"] = "timezone"


class AddressModel(BaseModel):
    """The class for representing an address."""

    city: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
    state: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
    zipcode: str | None = Field(
        ..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL}
    )
    latitude: float | None = Field(..., alias=ADDRESS_LATITUDE_COLUMN)
    longitude: float | None = Field(..., alias=ADDRESS_LONGITUDE_COLUMN)
    housenumber: str | None = Field(
        ..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL}
    )
    weather: WeatherModel | None
    timezone: str = Field(
        ...,
        json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL},
        alias=ADDRESS_TIMEZONE_COLUMN,
    )
    country: str = Field(..., json_schema_extra={TYPE_KEY: FieldType.CATEGORICAL})
