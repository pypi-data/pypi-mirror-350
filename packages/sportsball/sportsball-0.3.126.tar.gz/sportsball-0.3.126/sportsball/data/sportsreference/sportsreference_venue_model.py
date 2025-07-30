"""Sports Reference venue model."""

# pylint: disable=duplicate-code
import datetime

import pytest_is_running
import requests_cache

from ...cache import MEMORY
from ..google.google_address_model import create_google_address_model
from ..venue_model import VenueModel


def _create_sportsreference_venue_model(
    venue_name: str | None, session: requests_cache.CachedSession, dt: datetime.datetime
) -> VenueModel | None:
    if not venue_name:
        return None
    address_model = create_google_address_model(venue_name, session, dt)
    return VenueModel(
        identifier=venue_name,
        name=venue_name,
        address=address_model,
        is_grass=None,
        is_indoor=None,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_sportsreference_venue_model(
    venue_name: str | None, session: requests_cache.CachedSession, dt: datetime.datetime
) -> VenueModel | None:
    return _create_sportsreference_venue_model(venue_name, session, dt)


def create_sportsreference_venue_model(
    venue_name: str | None, session: requests_cache.CachedSession, dt: datetime.datetime
) -> VenueModel | None:
    """Create a sports reference venue model."""
    if not pytest_is_running.is_running():
        return _cached_create_sportsreference_venue_model(venue_name, session, dt)
    with session.cache_disabled():
        return _create_sportsreference_venue_model(venue_name, session, dt)
