"""Combined weather model."""

from ..weather_model import WeatherModel
from .null_check import is_null


def create_combined_weather_model(
    weather_models: list[WeatherModel],
) -> WeatherModel | None:
    """Create a weather model by combining many weather models."""
    if not weather_models:
        return None
    temperature = None
    relative_humidity = None
    for weather_model in weather_models:
        weather_model_temperature = weather_model.temperature
        if not is_null(weather_model_temperature):
            temperature = weather_model_temperature
        weather_model_relative_humidity = weather_model.relative_humidity
        if not is_null(weather_model_relative_humidity):
            relative_humidity = weather_model_relative_humidity
    return WeatherModel(temperature=temperature, relative_humidity=relative_humidity)
