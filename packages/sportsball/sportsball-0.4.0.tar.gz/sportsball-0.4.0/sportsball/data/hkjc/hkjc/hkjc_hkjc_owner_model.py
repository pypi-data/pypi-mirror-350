"""HKJC HKJC owner model."""

import urllib.parse
from urllib.parse import urlparse

from ...owner_model import OwnerModel


def create_hkjc_hkjc_owner_model(
    url: str,
) -> OwnerModel:
    """Create an HKJC owner."""
    o = urlparse(url)
    query = urllib.parse.parse_qs(o.query)
    name = query["HorseOwner"][0]
    return OwnerModel(
        identifier=name,
        name=name,
    )
