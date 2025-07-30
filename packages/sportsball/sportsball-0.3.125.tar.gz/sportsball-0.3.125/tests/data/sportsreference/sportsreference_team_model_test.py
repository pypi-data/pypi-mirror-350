"""Tests for the sportsreference team model class."""
import datetime
import os
import unittest

import requests_mock
import requests_cache
from sportsball.data.sportsreference.sportsreference_team_model import create_sportsreference_team_model
from sportsball.data.league import League


class TestSportsReferenceTeamModel(unittest.TestCase):

    def setUp(self):
        self.session = requests_cache.CachedSession(backend="memory")
        self.dir = os.path.dirname(__file__)

    def test_identifier(self):
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "2025.html"), "rb") as f:
                m.get("https://www.sports-reference.com/cbb/schools/villanova/men/2025.html", content=f.read())
            m.get("https://news.google.com/rss/search?q=%22Villanova+Wildcats+Men%27s%22+%2B+%28sport+OR+ncaab+OR+%22NCAA+Division+I+Basketball%22%29+after%3A2010-10-08+before%3A2010-10-09&ceid=US:en&hl=en&gl=US")
            team_model = create_sportsreference_team_model(
                self.session,
                "https://www.sports-reference.com/cbb/schools/villanova/men/2025.html",
                datetime.datetime(2010, 10, 10, 10, 10, 00),
                League.NCAAB,
                set(),
                10.0,
                {},
                {},
                {},
                {},
                {},
                "",
            )
            self.assertEqual(team_model.identifier, "Villanova Wildcats Men's")

    def test_field_goals(self):
        url = "https://www.sports-reference.com/cbb/schools/villanova/men/2025.html"
        player_url = "https://www.sports-reference.com/cbb/players/eric-dixon-1.html"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "2025.html"), "rb") as f:
                m.get(url, content=f.read())
            with open(os.path.join(self.dir, "eric-dixon-1.html"), "rb") as f:
                m.get(player_url, content=f.read())
            team_model = create_sportsreference_team_model(
                self.session,
                url,
                datetime.datetime(2010, 10, 10, 10, 10, 00),
                League.NCAAB,
                set([player_url]),
                10.0,
                {
                    "Eric Dixon": 8,
                },
                {},
                {},
                {},
                {},
                "",
            )
            self.assertEqual(team_model.field_goals, 8)

    def test_field_goals_attempted(self):
        url = "https://www.sports-reference.com/cbb/schools/villanova/men/2025.html"
        player_url = "https://www.sports-reference.com/cbb/players/eric-dixon-1.html"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "2025.html"), "rb") as f:
                m.get(url, content=f.read())
            with open(os.path.join(self.dir, "eric-dixon-1.html"), "rb") as f:
                m.get(player_url, content=f.read())
            team_model = create_sportsreference_team_model(
                self.session,
                url,
                datetime.datetime(2010, 10, 10, 10, 10, 00),
                League.NCAAB,
                set([player_url]),
                10.0,
                {
                    "Eric Dixon": 8,
                },
                {
                    "Eric Dixon": 10
                },
                {},
                {},
                {},
                "",
            )
            self.assertEqual(team_model.field_goals_attempted, 10)

    def test_identifier_2(self):
        url = "http://www.basketball-reference.com/teams/LAC/2015.html"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "LAC_2015.html"), "rb") as f:
                m.get(url, content=f.read())
            team_model = create_sportsreference_team_model(
                self.session,
                url,
                datetime.datetime(2010, 10, 10, 10, 10, 00),
                League.NCAAB,
                set(),
                10.0,
                {},
                {},
                {},
                {},
                {},
                "",
            )
            self.assertEqual(team_model.identifier, "Los Angeles Clippers")

    def test_identifier_3(self):
        url = "http://www.basketball-reference.com/teams/BRK/2014.html"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "BRK_2014.html"), "rb") as f:
                m.get(url, content=f.read())
            team_model = create_sportsreference_team_model(
                self.session,
                url,
                datetime.datetime(2010, 10, 10, 10, 10, 00),
                League.NCAAB,
                set(),
                10.0,
                {},
                {},
                {},
                {},
                {},
                "",
            )
            self.assertEqual(team_model.identifier, "Brooklyn Nets")

    def test_name(self):
        url = "http://www.basketball-reference.com/teams/CLE/2016.html"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "CLE_2016.html"), "rb") as f:
                m.get(url, content=f.read())
            team_model = create_sportsreference_team_model(
                self.session,
                url,
                datetime.datetime(2010, 10, 10, 10, 10, 00),
                League.NCAAB,
                set(),
                10.0,
                {},
                {},
                {},
                {},
                {},
                "",
            )
            self.assertEqual(team_model.name, "Cleveland Cavaliers")

    def test_name_2(self):
        url = "http://www.basketball-reference.com/teams/LAL/2015.html"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "LAL_2015.html"), "rb") as f:
                m.get(url, content=f.read())
            team_model = create_sportsreference_team_model(
                self.session,
                url,
                datetime.datetime(2010, 10, 10, 10, 10, 00),
                League.NBA,
                set(),
                10.0,
                {},
                {},
                {},
                {},
                {},
                "",
            )
            self.assertEqual(team_model.name, "Los Angeles Lakers")

    def test_name_3(self):
        url = "https://www.basketball-reference.com/teams/BOS/2015.html"
        with requests_mock.Mocker() as m:
            with open(os.path.join(self.dir, "BOS_2015.html"), "rb") as f:
                m.get(url, content=f.read())
            team_model = create_sportsreference_team_model(
                self.session,
                url,
                datetime.datetime(2010, 10, 10, 10, 10, 00),
                League.NBA,
                set(),
                10.0,
                {},
                {},
                {},
                {},
                {},
                "",
            )
            self.assertEqual(team_model.name, "Boston Celtics")
