# sportsball

<a href="https://pypi.org/project/sportsball/">
    <img alt="PyPi" src="https://img.shields.io/pypi/v/sportsball">
</a>

A library for pulling in and normalising sports stats.

<p align="center">
    <img src="sportsball.png" alt="sportsball" width="200"/>
</p>

## Dependencies :globe_with_meridians:

Python 3.11.6:

- [pandas](https://pandas.pydata.org/)
- [requests](https://requests.readthedocs.io/en/latest/)
- [requests-cache](https://requests-cache.readthedocs.io/en/stable/)
- [python-dateutil](https://github.com/dateutil/dateutil)
- [tqdm](https://github.com/tqdm/tqdm)
- [beautifulsoup](https://www.crummy.com/software/BeautifulSoup/)
- [openpyxl](https://openpyxl.readthedocs.io/en/stable/)
- [joblib](https://joblib.readthedocs.io/en/stable/)
- [pyarrow](https://arrow.apache.org/docs/python/index.html)
- [ipython](https://ipython.org/)
- [pytz](https://pythonhosted.org/pytz/)
- [python-dotenv](https://github.com/theskumar/python-dotenv)
- [geocoder](https://geocoder.readthedocs.io/)
- [retry-requests](https://github.com/bustawin/retry-requests)
- [timezonefinder](https://timezonefinder.michelfe.it/gui)
- [nba_api](https://github.com/swar/nba_api)
- [pydantic](https://docs.pydantic.dev/latest/)
- [flatten_json](https://github.com/amirziai/flatten)
- [pygooglenews](https://github.com/kotartemiy/pygooglenews)
- [extruct](https://github.com/scrapinghub/extruct)
- [wikipedia-api](https://github.com/martin-majlis/Wikipedia-API)
- [tweepy](https://www.tweepy.org/)
- [pytest-is-running](https://github.com/adamchainz/pytest-is-running)
- [PySocks](https://github.com/Anorov/PySocks)
- [func-timeout](https://github.com/kata198/func_timeout)
- [tenacity](https://github.com/jd/tenacity)
- [random_user_agent](https://github.com/Luqman-Ud-Din/random_user_agent)
- [wayback](https://github.com/edgi-govdata-archiving/wayback)
- [cryptography](https://cryptography.io/en/latest/)
- [feedparser](https://github.com/kurtmckee/feedparser)
- [dateparser](https://dateparser.readthedocs.io/en/latest/)
- [playwright](https://playwright.dev/)
- [cchardet](https://github.com/PyYoshi/cChardet)
- [lxml](https://lxml.de/)

## Raison D'être :thought_balloon:

`sportsball` aims to be a library for pulling in historical information about previous sporting games in a standardised fashion for easy data processing.
The models it uses are designed to be used for many different types of sports.

The supported leagues are:

* 🏉 [AFL](https://www.afl.com.au/)
* 🏀 [NBA](https://www.nba.com/)
* 🏀 [NCAAB](https://www.ncaa.com/sports/basketball-men/d1)
* 🏈 [NCAAF](https://www.ncaa.com/sports/football/fbs)
* 🏈 [NFL](https://www.nfl.com/)

## Architecture :triangular_ruler:

`sportsball` is an object orientated library. The entities are organised like so:

* **Game**: A game within a season.
    * **Team**: The team within the game. Note that in games with individual players a team exists as a wrapper.
        * **Player**: A player within the team.
        * **Odds**: The odds for the team to win the game.
            * **Bookie**: The bookie publishing the odds.
        * **News**: News about the team the day before the game.
        * **Social**: Social posts from the team the day before the game.
    * **Venue**: The venue the game was played in.
        * **Address**: The address information of a venue.
            * **Weather**: The weather at the address.

### Objects

A list of the attributes on each object.

#### Game

A representation of the game within a season.

* **dt**: The timezone aware date/time of the game start.
* **week**: The round of the game within the season.
* **game_number**: The index of the game within the round.
* **venue**: The venue the game took place at.
* **teams**: A list of teams within the game.
* **home_team**: The team representing the home team.
* **away_team**: The ream representing the away team.
* **end_dt**: The timzone aware date/time of the game end.
* **attendance**: How many people attended the game.
* **league**: The league the game belongs to.
* **year** The year the game was in.
* **season_type**: The type of the season the game was played in.
* **postponed**: Whether the game was postponed.
* **playoff**: Whether the game was a playoff game.

#### Team

A representation of a team within a game.

* **identifier**: The unique identifier for the team.
* **name**: The name of the team.
* **location**: The home location of the team.
* **players**: A list of players with the team for the game.
* **odds**: A list of odds for the team on the game to win.
* **points**: The amount of points scored by this team on the game.
* **ladder_rank**: The ladder rank of the team at the beginning of the round of the game.
* **kicks**: The number of kicks a team produced.
* **news**: News articles about the team a day from the game.
* **social**: Social media posts from the team a day from the game.
* **field_goals**: The sum of the field goals made by the team in the game.
* **field_goals_attempted**: The sum of the field goals attempted by the team in the game.
* **offensive_rebounds**: The number of rebounds during offense by the team in the game.
* **assists**: The number of times the player on the team made a pass that resulted in a field goal in the game.
* **turnovers**: The number of times a player on the team loses possession of the ball in the game.

#### Player

A representation of a player within a team within a game.

* **identifier**: The unique identifier for the player.
* **jersey**: The jersey identifying the player.
* **kicks**: The number of kicks the player made in the game.
* **fumbles**: The number of times the player fumbled the ball in the game.
* **fumbles_lost**: The number of times the player loses possession of the ball due to a fumble and the opposing team recovers the ball.
* **field_goals**: The number of field goals the player made in the game.
* **field_goals_attempted**: The number of field goal attempts the player made in the game.
* **offensive_rebounds**: The number of rebounds during offense by the player made in the game.
* **assists**: The number of times the player made a pass that resulted in a field goal in the game.
* **turnovers**: The number of times a player loses possession of the ball in the game.
* **name**: The name of the player.
* **marks**: The number of marks the player performed in the game.
* **handballs**: The number of handballs the player performed in the game.
* **disposals**: The number of disposals the player performed in the game.
* **goals**: The number of goals scored by the player in the game.
* **behinds**: The number of behinds scored by the player in the game.
* **hit_outs**: The number of hit outs scored by the player in the game.
* **tackles**: The number of tackles performed by the player in the game.
* **rebounds**: The number of rebounds performed by the player in the game.
* **insides**: The number of insides performed by the player in the game.
* **clearances**: The number of clearances performed by the player in the game.
* **clangers**: The number of clangers performed by the player in the game.
* **free_kicks_for**: The number of free kicks given to the player in the game.
* **free_kicks_against**: The number of free kicks given against an action taken by the player in the game.
* **brownlow_votes**: The number of votes for the brownlow medal the player has in the current season.
* **contested_possessions**: The number of possessions the player had in the game that were contested.
* **uncontested_possessions**: The number of posessions the player had in the game that were uncontested.
* **contested_marks**: The number of marks the player had in the game that were contested.
* **marks_inside**: The number of marks the player had in the game inside the 50.
* **one_percenters:** The number of times the player spoils, knock-ons, smothers or shepherds the ball during the game.
* **bounces**: The number of bounces the player makes in the game.
* **goal_assists**: The number of assists on goal the player had in the game.
* **percentage_played**: The percentage of the game the player was on the field.

#### Odds

A representation of the odds for a team to win within a game.

* **odds**: The decimal odds offered by a bookie for the team to win in the game.
* **bookie**: The bookie offering these odds.
* **dt**: When the odds were posted.

#### Venue

The venue the game is played at.

* **identifier**: The unique identifier for the venue.
* **names**: The name of the venue.
* **address**: The address of the venue.
* **is_grass**: Whether the venue has a grass field.
* **is_indoor**: Whether the venue is indoors.

#### Address

The address of the venue.

* **city**: The city of the address.
* **state**: The state of the address.
* **zipcode**: The postal/zip code of the address.
* **latitude**: The latitude of the address.
* **longitude**: The longitude of the address.
* **housenumber**: The house/street number of the address.
* **weather**: The weather at the address at the game start time.
* **timezone**: The time zone at the address.
* **country**: The country of the address.

#### Weather

The forecasted weather one day out at the address of the game start time.

* **temperature**: The temperature at the address at the game start time.
* **relative_humidity**: The relative humidity at the address at the game start time.

#### News

The news one day out from the game.

* **title**: The title of the article
* **published**: When the article was published.
* **summary**: The summary of the article.
* **source**: The source of the article.

#### Social

Social media posts one day out from the game.

* **network**: The social network this post was made from.
* **post**: The text of the post.
* **comments**: The number of comments on the post.
* **reposts**: The number of reposts.
* **likes**: The number of likes the post received.
* **views**: The number of views the post has.
* **published**: When the post was published.

## Caching

This library uses very aggressive caching due to the large data requirements. If the requests are about a recent game (generally in the last 7 days) the caching is bypassed. The caching is as follows:

1. A joblib disk cache that caches calls to pydantic model creation functions. This changes on every version update to keep the models in sync. This is the fastest cache.
2. A requests cache backed by sqlite that caches requests forever.
3. An attempt to find the response is made to the wayback machine, and used if found.

It's very recommended that the user uses proxies defined in the `PROXIES` environment variable. The more proxies the easier it is to collect data.

## Installation :inbox_tray:

This is a python package hosted on pypi, so to install simply run the following command:

`pip install sportsball`

or install using this local repository:

`python setup.py install --old-and-unmanageable`

## Usage example :eyes:

There are many different ways of using sportsball, but we generally recommend the CLI.

### CLI

To fetch a dataframe containing information about a league, you can use the following CLI:

```
sportsball --league=nfl -
```

The final argument denotes the file to write to, in this case `-` is stdout.

### Python

To pull a dataframe containing all the information for a particular league, the following example can be used:

```python
from sportsball import sportsball as spb

ball = spb.SportsBall()
league = ball.league(spb.League.AFL)
df = league.to_frame()
```

This results in a dataframe where each game is represented by all its features.

### Environment

If you wish to use the providers that require API keys, you can create a `.env` file with the following variables inside it:

```
GOOGLE_API_KEY=APIKEY
GRIBSTREAM_API_KEY=APIKEY
X_API_KEY=APIKEY
X_API_SECRET_KEY=APISECRETKEY
X_ACCESS_TOKEN=ACCESSTOKEN
X_ACCESS_TOKEN_SECRET=ACCESSTOKENSECRET
PROXIES=CSVPROXIESLIST
```

## License :memo:

The project is available under the [MIT License](LICENSE).
