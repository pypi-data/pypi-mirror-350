"""Tests for the sportsreference player model class."""
import datetime
import os
import unittest

import requests_mock
import requests_cache
from sportsball.data.sportsreference.sportsreference_player_model import create_sportsreference_player_model


class TestSportsReferencePlayerModel(unittest.TestCase):

    def setUp(self):
        self.session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_field_goals(self):
        url = "https://www.basketball-reference.com/players/b/barnesc01.html"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "barnesc01.html"), "rb") as f:
                m.get(url, content=f.read())
            player_model = create_sportsreference_player_model(
                self.session,
                url,
                datetime.datetime(2010, 10, 10, 10, 10, 0),
                {"Scottie Barnes": 8},
                {},
                {},
                {},
                {},
            )
            self.assertEqual(player_model.field_goals, 8)
