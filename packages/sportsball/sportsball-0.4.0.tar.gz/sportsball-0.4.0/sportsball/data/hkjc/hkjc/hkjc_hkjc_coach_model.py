"""HKJC HKJC coach model."""

import io

import pandas as pd
import pytest_is_running
import requests_cache

from ....cache import MEMORY
from ....proxy_session import X_NO_WAYBACK
from ...coach_model import CoachModel


def _create_hkjc_hkjc_coach_model(
    session: requests_cache.CachedSession,
    url: str,
) -> CoachModel:
    headers = {X_NO_WAYBACK: "1"}
    response = session.get(url, headers=headers)
    response.raise_for_status()

    handle = io.StringIO()
    handle.write(response.text)
    handle.seek(0)
    dfs = pd.read_html(handle)

    name = None
    age = None
    for count, df in enumerate(dfs):
        if count == 0:
            name = df.iat[0, 0].strip()
            age = int(df.iat[1, 0].strip().split(":")[-1].strip())

    if name is None:
        raise ValueError("name is null")

    return CoachModel(
        identifier=name,
        name=name,
        birth_date=None,
        age=age,
    )


@MEMORY.cache(ignore=["session"])
def _cached_create_hkjc_hkjc_coach_model(
    session: requests_cache.CachedSession,
    url: str,
) -> CoachModel:
    return _create_hkjc_hkjc_coach_model(session=session, url=url)


def create_hkjc_hkjc_coach_model(
    session: requests_cache.CachedSession,
    url: str,
) -> CoachModel:
    """Create a coach model based off HKJC."""
    if not pytest_is_running.is_running():
        return _cached_create_hkjc_hkjc_coach_model(session=session, url=url)
    return _create_hkjc_hkjc_coach_model(session=session, url=url)
