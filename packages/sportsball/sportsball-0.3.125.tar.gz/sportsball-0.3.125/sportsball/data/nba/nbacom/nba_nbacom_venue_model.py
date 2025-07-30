"""NBA NBA.com venue model."""

# pylint: disable=too-many-statements,protected-access
import datetime

import requests_cache

from ...google.google_address_model import create_google_address_model
from ...venue_model import VenueModel


def create_nba_nbacom_venue_model(
    venue_name: str,
    session: requests_cache.CachedSession,
    dt: datetime.datetime,
) -> VenueModel:
    """Create a game model from AFL Tables."""
    address_model = create_google_address_model(venue_name, session, dt)
    return VenueModel(
        identifier=venue_name,
        name=venue_name,
        address=address_model,
        is_grass=None,
        is_indoor=None,
    )
