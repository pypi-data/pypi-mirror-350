"""HKJC HKJC player model."""

# pylint: disable=too-many-arguments,duplicate-code,too-many-locals,too-many-branches,too-many-statements
import io
import logging
import urllib.parse
from urllib.parse import urlparse

import pandas as pd
import pytest_is_running
import requests_cache
from bs4 import BeautifulSoup

from ....cache import MEMORY
from ....proxy_session import X_NO_WAYBACK
from ...google.google_address_model import create_google_address_model
from ...player_model import PlayerModel
from ...sex import sex_from_str
from ...species import Species
from ..position import Position
from .hkjc_hkjc_owner_model import create_hkjc_hkjc_owner_model


def _create_hkjc_hkjc_player_model(
    session: requests_cache.CachedSession,
    url: str,
    jersey: str | None,
    handicap_weight: float | None,
    starting_position: Position | None,
    weight: float | None,
) -> PlayerModel:
    headers = {X_NO_WAYBACK: "1"}
    response = session.get(url, headers=headers)
    response.raise_for_status()
    handle = io.StringIO()
    handle.write(response.text)
    handle.seek(0)
    dfs = []
    try:
        dfs = pd.read_html(handle)
    except AttributeError as exc:
        logging.warning(str(exc))
    o = urlparse(url)
    soup = BeautifulSoup(response.text, "lxml")

    name = None
    species = Species.HUMAN
    father = None
    sex = None
    age = None
    birth_address = None
    owner = None
    if o.path.endswith("/Horse/Horse.aspx"):
        species = Species.HORSE
        for count, df in enumerate(dfs):
            if count == 0:
                name = df.iat[1, 0].strip().split("(")[0].strip()

                sex_row = None
                origin_row = None
                for i in range(1, len(df)):
                    row_name = str(df.iat[i, 0]).strip().lower()
                    if "sex" in row_name:
                        sex_row = i
                    elif "origin" in row_name:
                        origin_row = i

                sex = sex_from_str(df.iat[sex_row, 2].strip().split("/")[-1].strip())

                origin_str = df.iat[origin_row, 2].strip()
                origin = None
                age = None
                if "/" in origin_str:
                    origin, age_str = origin_str.split("/")
                    age = int(age_str.strip())
                else:
                    origin = origin_str
                origin = origin.strip()

                birth_address = create_google_address_model(
                    query=origin.strip(), session=session, dt=None
                )
        for a in soup.find_all("a", href=True):
            a_url = urllib.parse.urljoin(url, a.get("href"))
            a_o = urlparse(a_url)
            if a_o.path.endswith("Horse/SameSire.aspx"):
                father = create_hkjc_hkjc_player_model(
                    session=session,
                    url=a_url,
                    jersey=None,
                    handicap_weight=None,
                    starting_position=None,
                    weight=None,
                )
            elif a_o.path.endswith("Horse/OwnerSearch.aspx"):
                owner = create_hkjc_hkjc_owner_model(a_url)
    elif o.path.endswith("Jockey/JockeyProfile.aspx"):
        for count, df in enumerate(dfs):
            if count == 0:
                name = df.iat[0, 0].strip()
                age = int(df.iat[1, 0].strip().split(":")[-1].strip())
    elif o.path.endswith("Horse/SameSire.aspx"):
        species = Species.HORSE
        query = urllib.parse.parse_qs(o.query)
        name = query["HorseSire"][0]

    if name is None:
        raise ValueError("name is null")

    return PlayerModel(
        identifier=name,
        jersey=jersey,
        kicks=None,
        fumbles=None,
        fumbles_lost=None,
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
        birth_date=None,
        species=str(species),
        handicap_weight=handicap_weight,
        father=father,
        sex=str(sex) if sex is not None else None,
        age=age,
        starting_position=str(starting_position)
        if starting_position is not None
        else None,
        weight=weight,
        birth_address=birth_address,
        owner=owner,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_hkjc_hkjc_player_model(
    session: requests_cache.CachedSession,
    url: str,
    jersey: str | None,
    handicap_weight: float | None,
    starting_position: Position | None,
    weight: float | None,
) -> PlayerModel:
    return _create_hkjc_hkjc_player_model(
        session=session,
        url=url,
        jersey=jersey,
        handicap_weight=handicap_weight,
        starting_position=starting_position,
        weight=weight,
    )


def create_hkjc_hkjc_player_model(
    session: requests_cache.CachedSession,
    url: str,
    jersey: str | None,
    handicap_weight: float | None,
    starting_position: Position | None,
    weight: float | None,
) -> PlayerModel:
    """Create a player model based off HKJC."""
    if not pytest_is_running.is_running():
        return _cached_create_hkjc_hkjc_player_model(
            session=session,
            url=url,
            jersey=jersey,
            handicap_weight=handicap_weight,
            starting_position=starting_position,
            weight=weight,
        )
    return _create_hkjc_hkjc_player_model(
        session=session,
        url=url,
        jersey=jersey,
        handicap_weight=handicap_weight,
        starting_position=starting_position,
        weight=weight,
    )
