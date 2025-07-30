"""ESPN player model."""

# pylint: disable=duplicate-code
import datetime
from typing import Any

import pytest_is_running
import requests_cache
from dateutil.parser import parse

from ...cache import MEMORY
from ..player_model import PlayerModel


def _create_espn_player_model(
    session: requests_cache.CachedSession, player: dict[str, Any]
) -> PlayerModel:
    identifier = str(player["playerId"])
    jersey = player.get("jersey")
    fumbles = None
    fumbles_lost = None
    if "statistics" in player:
        statistics_response = session.get(player["statistics"]["$ref"])
        if statistics_response.ok:
            statistics_dict = statistics_response.json()
            fumbles = None
            for category in statistics_dict["splits"]["categories"]:
                for stat in category["stats"]:
                    if stat["name"] == "fumbles":
                        fumbles = stat["value"]
                    if stat["name"] == "fumblesLost":
                        fumbles_lost = stat["value"]
    athlete_response = session.get(player["athlete"]["$ref"])
    athlete_response.raise_for_status()
    athlete_dict = athlete_response.json()
    name = athlete_dict["fullName"]
    birth_date = parse(athlete_dict["dateOfBirth"]).date()
    return PlayerModel(
        identifier=identifier,
        jersey=jersey,
        kicks=None,
        fumbles=fumbles,
        fumbles_lost=fumbles_lost,
        field_goals=None,
        field_goals_attempted=None,
        offensive_rebounds=None,
        assists=None,
        turnovers=None,
        name=name,
        marks=None,
        handballs=None,
        disposals=None,
        goals=None,
        behinds=None,
        hit_outs=None,
        tackles=None,
        rebounds=None,
        insides=None,
        clearances=None,
        clangers=None,
        free_kicks_for=None,
        free_kicks_against=None,
        brownlow_votes=None,
        contested_possessions=None,
        uncontested_possessions=None,
        contested_marks=None,
        marks_inside=None,
        one_percenters=None,
        bounces=None,
        goal_assists=None,
        percentage_played=None,
        birth_date=birth_date,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_espn_player_model(
    session: requests_cache.CachedSession, player: dict[str, Any]
) -> PlayerModel:
    return _create_espn_player_model(session, player)


def create_espn_player_model(
    session: requests_cache.CachedSession, player: dict[str, Any], dt: datetime.datetime
) -> PlayerModel:
    """Create a player model based off ESPN."""
    if (
        not pytest_is_running.is_running()
        and dt < datetime.datetime.now() - datetime.timedelta(days=7)
    ):
        return _cached_create_espn_player_model(session, player)
    with session.cache_disabled():
        return _create_espn_player_model(session, player)
