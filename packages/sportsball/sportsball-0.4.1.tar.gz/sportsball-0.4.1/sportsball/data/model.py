"""The base class for a data model."""

# pylint: disable=too-few-public-methods
import pandas as pd
import requests_cache

from ..proxy_session import create_proxy_session


class Model:
    """The base model class."""

    _session: requests_cache.CachedSession | None

    def __init__(self, session: requests_cache.CachedSession) -> None:
        self._session = session

    @property
    def session(self) -> requests_cache.CachedSession:
        """Fetch a session that can never be null."""
        session = self._session
        if session is None:
            session = create_proxy_session()
            self._session = session
        return session

    def clear_session(self):
        """Clear the session."""
        self._session = None

    def to_frame(self) -> pd.DataFrame:
        """Render the model as a dataframe."""
        raise NotImplementedError("to_frame not implemented by parent class.")
