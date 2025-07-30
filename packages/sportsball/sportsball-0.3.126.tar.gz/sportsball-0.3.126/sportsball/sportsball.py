"""The main sportsball class for accessing data."""

from typing import Dict
from warnings import simplefilter

import pandas as pd
import requests_cache
from dotenv import load_dotenv

from .data.afl import AFLLeagueModel
from .data.league import League
from .data.league_model import LeagueModel
from .data.nba import NBALeagueModel
from .data.ncaab import NCAABLeagueModel
from .data.ncaaf import NCAAFLeagueModel
from .data.nfl import NFLLeagueModel
from .proxy_session import create_proxy_session


class SportsBall:
    """The main sportsball class."""

    # pylint: disable=too-few-public-methods

    _leagues: Dict[str, LeagueModel]
    _session: requests_cache.CachedSession

    def __init__(self) -> None:
        self._session = create_proxy_session()
        self._leagues = {}
        simplefilter(action="ignore", category=pd.errors.PerformanceWarning)
        load_dotenv()

    def league(self, league: League, league_filter: str | None) -> LeagueModel:
        """Provide a league model for the given league."""
        if league not in self._leagues:
            if league == League.NFL:
                self._leagues[league] = NFLLeagueModel(self._session, league_filter)
            elif league == League.AFL:
                self._leagues[league] = AFLLeagueModel(self._session, league_filter)
            elif league == League.NBA:
                self._leagues[league] = NBALeagueModel(self._session, league_filter)
            elif league == League.NCAAF:
                self._leagues[league] = NCAAFLeagueModel(self._session, league_filter)
            elif league == League.NCAAB:
                self._leagues[league] = NCAABLeagueModel(self._session, league_filter)
            else:
                raise ValueError(f"Unrecognised league: {league}")
        return self._leagues[league]
