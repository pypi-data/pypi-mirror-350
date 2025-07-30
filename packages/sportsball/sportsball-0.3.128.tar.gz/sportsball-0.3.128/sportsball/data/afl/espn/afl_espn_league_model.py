"""AFL ESPN league model."""

# pylint: disable=line-too-long

import requests_cache

from ...espn.espn_league_model import ESPNLeagueModel
from ...league import League

_SEASON_URL = "https://sports.core.api.espn.com/v2/sports/australian-football/leagues/afl/seasons?limit=100"


class AFLESPNLeagueModel(ESPNLeagueModel):
    """AFL ESPN implementation of the league model."""

    def __init__(
        self, session: requests_cache.CachedSession, position: int | None = None
    ) -> None:
        super().__init__(_SEASON_URL, League.AFL, session, position=position)
