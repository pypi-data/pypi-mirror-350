"""NFL OddsPortal league model."""

# pylint: disable=line-too-long

import requests_cache

from ...league import League
from ...oddsportal.oddsportal_league_model import OddsPortalLeagueModel


class NFLOddsPortalLeagueModel(OddsPortalLeagueModel):
    """NFL OddsPortal implementation of the league model."""

    def __init__(
        self, session: requests_cache.CachedSession, position: int | None = None
    ) -> None:
        super().__init__(League.NFL, session, position=position)

    @classmethod
    def name(cls) -> str:
        return "nfl-oddsportal-league-model"
