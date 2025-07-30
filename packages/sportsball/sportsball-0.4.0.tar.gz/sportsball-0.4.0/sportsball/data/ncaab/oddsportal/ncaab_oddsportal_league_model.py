"""NCAAB OddsPortal league model."""

# pylint: disable=line-too-long

import requests_cache

from ...league import League
from ...oddsportal.oddsportal_league_model import OddsPortalLeagueModel


class NCAABOddsPortalLeagueModel(OddsPortalLeagueModel):
    """NCAAB OddsPortal implementation of the league model."""

    def __init__(
        self, session: requests_cache.CachedSession, position: int | None = None
    ) -> None:
        super().__init__(League.NCAAB, session, position=position)

    @classmethod
    def name(cls) -> str:
        return "ncaab-oddsportal-league-model"
