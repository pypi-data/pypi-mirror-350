"""NCAAF ESPN league model."""

# pylint: disable=line-too-long

import requests_cache

from ...espn.espn_league_model import ESPNLeagueModel
from ...league import League

_SEASON_URL = "http://sports.core.api.espn.com/v2/sports/football/leagues/college-football/seasons?limit=100"


class NCAAFESPNLeagueModel(ESPNLeagueModel):
    """NCAAF ESPN implementation of the league model."""

    def __init__(
        self, session: requests_cache.CachedSession, position: int | None = None
    ) -> None:
        super().__init__(_SEASON_URL, League.NCAAF, session, position=position)
