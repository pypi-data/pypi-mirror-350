"""Gribstream weather model."""

import datetime
import gzip
import io
import json
import os

import pandas as pd
import pytest_is_running
import pytz
import requests
import requests_cache

from ....cache import MEMORY
from ...weather_model import WeatherModel


def _create_gribstream_weather_model(
    session: requests_cache.CachedSession,
    latitude: float,
    longitude: float,
    dt: datetime.datetime,
) -> WeatherModel | None:
    api_key = os.environ.get("GRIBSTREAM_API_KEY")
    if api_key is None:
        return None
    url = "https://gribstream.com/api/v2/nbm/forecasts"
    payload = {
        "forecastedFrom": dt.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "forecastedUntil": dt.astimezone(pytz.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "minHorizon": 12,
        "maxHorizon": 24,
        "coordinates": [{"lat": latitude, "lon": longitude}],
        "variables": [
            {"name": "TMP", "level": "2 m above ground", "info": ""},
            {"name": "DPT", "level": "2 m above ground", "info": ""},
            {"name": "RH", "level": "2 m above ground", "info": ""},
        ],
    }
    try:
        resp = session.post(
            url,
            data=gzip.compress(json.dumps(payload).encode("utf-8")),
            headers={
                "Accept-Encoding": "gzip",
                "Content-Encoding": "gzip",
                "Content-Type": "application/json",
                "Authorization": "Bearer ",
            },
        )
    except requests.exceptions.ConnectionError:
        return None
    if not resp.ok:
        return None
    df = pd.read_csv(io.BytesIO(resp.content), parse_dates=[0, 1])
    idx = df.index.get_indexer([dt], method="nearest")[0]
    temperature = df.iloc[idx]["TMP|2 m above ground|"]  # type: ignore
    relative_humidity = df.iloc[idx]["RH|2 m above ground|"]  # type: ignore
    return WeatherModel(temperature=temperature, relative_humidity=relative_humidity)


@MEMORY.cache(ignore=["session"])
def _cached_create_gribstream_weather_model(
    session: requests_cache.CachedSession,
    latitude: float,
    longitude: float,
    dt: datetime.datetime,
) -> WeatherModel | None:
    return _create_gribstream_weather_model(session, latitude, longitude, dt)


def create_gribstream_weather_model(
    session: requests_cache.CachedSession,
    latitude: float,
    longitude: float,
    dt: datetime.datetime,
) -> WeatherModel | None:
    """Create a weather model from gribstream."""
    if not pytest_is_running.is_running() and dt < datetime.datetime.now().replace(
        tzinfo=dt.tzinfo
    ) - datetime.timedelta(days=3):
        return _cached_create_gribstream_weather_model(session, latitude, longitude, dt)
    with session.cache_disabled():
        return _create_gribstream_weather_model(session, latitude, longitude, dt)
