"""A class for holding weather information."""

from pydantic import BaseModel


class WeatherModel(BaseModel):
    """The serialisable class for representing weather."""

    temperature: float | None
    relative_humidity: float | None
