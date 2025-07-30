"""ESPN player model."""

# pylint: disable=duplicate-code,too-many-locals
import datetime
from typing import Any

import pytest_is_running
import requests_cache
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from ...cache import MEMORY
from ..google.google_address_model import create_google_address_model
from ..player_model import PlayerModel
from ..sex import Sex
from ..species import Species


def _create_espn_player_model(
    session: requests_cache.CachedSession,
    player: dict[str, Any],
    positions_validator: dict[str, str],
    dt: datetime.datetime,
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
    position_response = session.get(player["position"]["$ref"])
    position_response.raise_for_status()
    position_dict = position_response.json()
    name = athlete_dict["fullName"]
    birth_date = parse(athlete_dict["dateOfBirth"]).date()
    birth_place = athlete_dict["birthPlace"]
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
        species=str(Species.HUMAN),
        handicap_weight=None,
        father=None,
        sex=str(Sex.MALE),
        age=None if birth_date is None else relativedelta(birth_date, dt).years,
        starting_position=positions_validator[position_dict["abbreviation"]],
        weight=athlete_dict["weight"] * 0.453592,
        birth_address=create_google_address_model(
            query=", ".join(
                [birth_place["city"], birth_place["state"], birth_place["country"]]
            ),
            session=session,
            dt=None,
        ),
        owner=None,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_espn_player_model(
    session: requests_cache.CachedSession,
    player: dict[str, Any],
    positions_validator: dict[str, str],
    dt: datetime.datetime,
) -> PlayerModel:
    return _create_espn_player_model(
        session=session, player=player, positions_validator=positions_validator, dt=dt
    )


def create_espn_player_model(
    session: requests_cache.CachedSession,
    player: dict[str, Any],
    dt: datetime.datetime,
    positions_validator: dict[str, str],
) -> PlayerModel:
    """Create a player model based off ESPN."""
    if (
        not pytest_is_running.is_running()
        and dt < datetime.datetime.now() - datetime.timedelta(days=7)
    ):
        return _cached_create_espn_player_model(
            session=session,
            player=player,
            positions_validator=positions_validator,
            dt=dt,
        )
    with session.cache_disabled():
        return _create_espn_player_model(
            session=session,
            player=player,
            positions_validator=positions_validator,
            dt=dt,
        )
