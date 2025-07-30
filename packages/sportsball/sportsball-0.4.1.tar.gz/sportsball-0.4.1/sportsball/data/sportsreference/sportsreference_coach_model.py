"""Sports reference coach model."""

# pylint: disable=duplicate-code
import datetime
import logging
import os
from urllib.parse import urlparse

import pytest_is_running
import requests_cache
from bs4 import BeautifulSoup
from dateutil.parser import parse
from dateutil.relativedelta import relativedelta

from ...cache import MEMORY
from ...proxy_session import X_NO_WAYBACK
from ..coach_model import CoachModel

_NON_WAYBACK_URLS: set[str] = {
    "https://www.sports-reference.com/cbb/coaches/kelvin-sampson-1.html",
    "https://www.sports-reference.com/cbb/coaches/fred-hoiberg-1.html",
    "https://www.sports-reference.com/cbb/coaches/johnny-dawkins-1.html",
    "https://www.sports-reference.com/cbb/coaches/bruce-pearl-1.html",
    "https://www.sports-reference.com/cbb/coaches/leon-rice-1.html",
    "https://www.sports-reference.com/cbb/coaches/wes-miller-1.html",
    "https://www.sports-reference.com/cbb/coaches/dan-earl-1.html",
}


def _create_sportsreference_coach_model(
    session: requests_cache.CachedSession, coach_url: str, dt: datetime.datetime
) -> CoachModel:
    """Create a coach model from sports reference."""
    headers = {}
    if coach_url in _NON_WAYBACK_URLS:
        headers = {X_NO_WAYBACK: "1"}
    response = session.get(coach_url, headers=headers)
    response.raise_for_status()
    soup = BeautifulSoup(response.text, "lxml")

    name = None
    for h1 in soup.find_all("h1"):
        for span in h1.find_all("span"):
            name = span.get_text().strip()
            break
        if name is not None:
            break

    if name is None:
        for h1 in soup.find_all("h1"):
            name = h1.get_text().strip()

    if name is None:
        logging.error(response.text)
        logging.error("error url = %s", coach_url)
        raise ValueError("name is null")

    birth_date = None
    for span in soup.find_all("span", {"id": "necro-birth"}):
        birth_date = parse(span.get("data-birth"))

    o = urlparse(coach_url)
    last_component = o.path.split("/")[-1]
    identifier, _ = os.path.splitext(last_component)
    return CoachModel(
        identifier=identifier,
        name=name,
        birth_date=birth_date,
        age=None if birth_date is None else relativedelta(birth_date, dt).years,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_sportsreference_coach_mode(
    session: requests_cache.CachedSession, coach_url: str, dt: datetime.datetime
) -> CoachModel:
    return _create_sportsreference_coach_model(
        session=session, coach_url=coach_url, dt=dt
    )


def create_sportsreference_coach_model(
    session: requests_cache.CachedSession, coach_url: str, dt: datetime.datetime
) -> CoachModel:
    """Create a coach model from sports reference."""
    if not pytest_is_running.is_running():
        return _cached_create_sportsreference_coach_mode(
            session=session, coach_url=coach_url, dt=dt
        )
    with session.cache_disabled():
        return _create_sportsreference_coach_model(
            session=session, coach_url=coach_url, dt=dt
        )
