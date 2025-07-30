"""NBA Sports DB league model."""

import requests_cache

from ...league import League
from ...sportsdb.sportsdb_league_model import SportsDBLeagueModel


class NBASportsDBLeagueModel(SportsDBLeagueModel):
    """NBA SportsDB implementation of the league model."""

    def __init__(
        self, session: requests_cache.CachedSession, position: int | None = None
    ) -> None:
        super().__init__(session, "4387", League.NBA, position=position)
