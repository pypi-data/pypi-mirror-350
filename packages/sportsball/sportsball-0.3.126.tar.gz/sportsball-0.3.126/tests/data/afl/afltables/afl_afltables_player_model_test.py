"""Tests for the afltables player model class."""
import datetime
import os
import unittest

import requests_mock
import requests_cache
from sportsball.data.afl.afltables.afl_afltables_player_model import create_afl_afltables_player_model


class TestAFLTablesPlayerModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_dt(self):
        dt = datetime.datetime(2023, 9, 15, 0, 15)
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "Dennis_Armfield.html"), "rb") as f:
                m.get("https://afltables.com/afl/stats/players/D/Dennis_Armfield.html", content=f.read())
            player_model = create_afl_afltables_player_model(
                "https://afltables.com/afl/stats/players/D/Dennis_Armfield.html",
                "35",
                10,
                self._session,
                "Dennis Armfield",
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0,
                0.0,
            )
            self.assertEqual(player_model.identifier, "Dennis_Armfield")
