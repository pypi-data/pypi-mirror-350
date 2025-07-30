"""Odds Portal venue model."""

import datetime

import pytest_is_running
import requests_cache

from ...cache import MEMORY
from ..google.google_address_model import create_google_address_model
from ..venue_model import VenueModel


def _create_oddsportal_venue_model(
    session: requests_cache.CachedSession,
    dt: datetime.datetime,
    venue: str,
    venue_town: str,
    venue_country: str,
) -> VenueModel | None:
    return VenueModel(
        identifier=venue,
        name=venue,
        address=create_google_address_model(
            ", ".join([venue, venue_town, venue_country]), session, dt
        ),
        is_grass=None,
        is_indoor=None,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_oddsportal_venue_model(
    session: requests_cache.CachedSession,
    dt: datetime.datetime,
    venue: str,
    venue_town: str,
    venue_country: str,
) -> VenueModel | None:
    return _create_oddsportal_venue_model(session, dt, venue, venue_town, venue_country)


def create_oddsportal_venue_model(
    session: requests_cache.CachedSession,
    dt: datetime.datetime,
    venue: str,
    venue_town: str,
    venue_country: str,
) -> VenueModel | None:
    """Create odds portal venue model."""
    if not pytest_is_running.is_running() and dt < datetime.datetime.now().replace(
        tzinfo=dt.tzinfo
    ) - datetime.timedelta(days=7):
        return _cached_create_oddsportal_venue_model(
            session, dt, venue, venue_town, venue_country
        )
    with session.cache_disabled():
        return _create_oddsportal_venue_model(
            session, dt, venue, venue_town, venue_country
        )
