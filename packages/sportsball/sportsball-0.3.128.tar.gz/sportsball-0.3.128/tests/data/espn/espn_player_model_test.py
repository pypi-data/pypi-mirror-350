"""Tests for the ESPN player model class."""
import datetime
import os
import unittest

import requests_mock
import requests_cache
from sportsball.data.espn.espn_player_model import create_espn_player_model


class TestESPNPlayerModel(unittest.TestCase):

    def setUp(self):
        self._session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_identifier(self):
        dt = datetime.datetime(2023, 9, 15, 0, 15)
        identifier = "a"
        statistics_url = "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/events/401671855/competitions/401671855/competitors/5/roster/16837/statistics/0?lang=en&region=us"
        athletes_url = "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/seasons/2024/athletes/16837?lang=en&region=us"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "16837_statistics.json"), "rb") as f:
                m.get(statistics_url, content=f.read())
            with open(os.path.join(self.dir, "16837_athletes.json"), "rb") as f:
                m.get(athletes_url, content=f.read())
            player_model = create_espn_player_model(
                self._session,
                {
                    "playerId": identifier,
                    "period": 0,
                    "active": False,
                    "starter": True,
                    "forPlayerId": 0,
                    "jersey": "93",
                    "valid": True,
                    "athlete": {
                        "$ref": athletes_url,
                    },
                    "position": {
                        "$ref": "http://sports.core.api.espn.com/v2/sports/football/leagues/nfl/positions/32?lang=en&region=us",
                    },
                    "statistics": {
                        "$ref": statistics_url,
                    },
                    "didNotPlay": False,
                    "displayName": "S. Harris",
                },
                dt,
            )

            self.assertEqual(player_model.identifier, identifier)
