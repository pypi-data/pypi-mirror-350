"""A class for handling windowed plackett luce ratings."""

# pylint: disable=too-many-locals,too-many-branches,too-many-statements,too-few-public-methods,too-many-nested-blocks

import datetime
import json
import os

import pandas as pd
from openskill.models import PlackettLuce, PlackettLuceRating

from .identifier import Identifier
from .match import Match
from .team import Team

_STATE_FILE = "state.json"
_TEAM_RATINGS_KEY = "team_ratings"
_MU_KEY = "mu"
_SIGMA_KEY = "sigma"
_NAME_KEY = "name"
_PLAYER_RATINGS_KEY = "player_ratings"
_MATCHES_KEY = "matches"
_PLAYERS_KEY = "players"
_TEAMS_KEY = "teams"
_POINTS_KEY = "points"
_IDENTIFIER_KEY = "identifier"
_DT_KEY = "dt"


class WindowedRating:
    """Handles plackett luce ratings based on windows."""

    _team_ratings: dict[str, PlackettLuceRating]
    _player_ratings: dict[str, PlackettLuceRating]
    _matches: list[Match]

    def __init__(self, window: datetime.timedelta | None, dt_column: str):
        self.window = window
        self._dt_column = dt_column
        self._team_model = PlackettLuce()
        self._player_model = PlackettLuce()
        self._team_ratings = {}
        self._player_ratings = {}
        self._matches = []

    @property
    def _state_file(self) -> str:
        window_str = "null" if self.window is None else str(self.window.days)
        state_file = "_".join([window_str, _STATE_FILE])
        return state_file

    def add(
        self,
        row: pd.Series,
        team_identifiers: list[Identifier],
        player_identifiers: list[Identifier],
    ) -> tuple[
        dict[str, tuple[PlackettLuceRating, int, float]],
        dict[str, tuple[PlackettLuceRating, int, float]],
    ]:
        """Add a new row to the windowed rating."""
        teams = []
        for team_identifier in team_identifiers:
            if team_identifier.column not in row:
                continue
            team_id = row[team_identifier.column]
            if pd.isnull(team_id):
                continue
            if team_id not in self._team_ratings:
                self._team_ratings[team_id] = self._team_model.rating(name=team_id)

            team_player_ids = []
            for player_identifier in player_identifiers:
                if player_identifier.team_identifier_column is None:
                    continue
                if player_identifier.team_identifier_column not in row:
                    continue
                player_team_id = row[player_identifier.team_identifier_column]
                if pd.isnull(player_team_id):
                    continue
                if player_team_id != team_id:
                    continue
                if player_identifier.column not in row:
                    continue
                player_id = row[player_identifier.column]
                if pd.isnull(player_id):
                    continue
                team_player_ids.append(player_id)
                if player_id not in self._player_ratings:
                    self._player_ratings[player_id] = self._player_model.rating(
                        name=player_id
                    )

            points = None
            if (
                team_identifier.points_column is not None
                and team_identifier.points_column in row
            ):
                points = row[team_identifier.points_column]
            teams.append(Team(team_player_ids, points, team_id))

        match = Match(teams, row[self._dt_column].to_pydatetime())

        if self.window is not None:
            # Remove older matches and reverse their results.
            oldest_dt = match.dt - self.window
            remove_matches = [x for x in self._matches if x.dt < oldest_dt]
            for remove_match in remove_matches:
                scores: list[float] | None = [
                    x.points
                    for x in reversed(remove_match.teams)
                    if x.points is not None
                ]
                if not scores:
                    scores = None
                if len(remove_match.teams) >= 2:
                    team_ratings: list[list[PlackettLuceRating]] = [
                        [self._team_ratings[x.identifier]] for x in remove_match.teams
                    ]
                    team_ratings = self._team_model.rate(
                        team_ratings,
                        scores=scores,
                    )
                    for team_rating in team_ratings:
                        self._team_ratings[str(team_rating[0].name)] = team_rating[0]
                    if all(x.players for x in remove_match.teams):
                        players = self._player_model.rate(
                            [
                                [self._player_ratings[y] for y in x.players]
                                for x in remove_match.teams
                            ],
                            scores=scores,
                        )
                        for player_rating in players:
                            for player_subrating in player_rating:
                                self._player_ratings[str(player_subrating.name)] = (
                                    player_subrating
                                )
            self._matches = self._matches[len(remove_matches) :]

        # Find the results
        team_result = {}
        player_result = {}
        if len(match.teams) >= 2:
            team_rank = self._team_model.predict_rank(
                [[self._team_ratings[x.identifier]] for x in match.teams]
            )
            team_result = {
                x.identifier: (
                    self._team_ratings[x.identifier],
                    team_rank[count][0],
                    team_rank[count][1],
                )
                for count, x in enumerate(match.teams)
            }
            if all(x.players for x in match.teams):
                player_rank = self._player_model.predict_rank(
                    [[self._player_ratings[y] for y in x.players] for x in match.teams]
                )
                for count, team in enumerate(match.teams):
                    for player in team.players:
                        player_result[player] = (
                            self._player_ratings[player],
                            player_rank[count][0],
                            player_rank[count][1],
                        )

        # Record the new match results
        scores = [x.points for x in match.teams if x.points is not None]
        if not scores:
            scores = None
        if len(match.teams) >= 2:
            team_ratings = self._team_model.rate(
                [[self._team_ratings[x.identifier]] for x in match.teams], scores=scores
            )
            for team_rating in team_ratings:
                self._team_ratings[str(team_rating[0])] = team_rating[0]
            if all(x.players for x in match.teams):
                player_ratings: list[list[PlackettLuceRating]] = (
                    self._player_model.rate(
                        [
                            [self._player_ratings[y] for y in x.players]
                            for x in match.teams
                        ],
                        scores=scores,
                    )
                )
                for player_rating in player_ratings:
                    for player_subrating in player_rating:
                        self._player_ratings[str(player_subrating.name)] = (
                            player_subrating
                        )
        self._matches.append(match)

        return team_result, player_result

    def load(self, folder: str) -> bool:
        """Loads the state from a folder."""
        state_file = os.path.join(folder, self._state_file)
        if not os.path.exists(state_file):
            return False
        team_ratings = {}
        player_ratings = {}
        matches = []
        with open(state_file, encoding="utf8") as handle:
            state = json.load(handle)
            for k, v in state[_TEAM_RATINGS_KEY].items():
                team_ratings[k] = PlackettLuceRating(
                    mu=v[_MU_KEY], sigma=v[_SIGMA_KEY], name=v[_NAME_KEY]
                )
            for k, v in state[_PLAYER_RATINGS_KEY].items():
                player_ratings[k] = PlackettLuceRating(
                    mu=v[_MU_KEY], sigma=v[_SIGMA_KEY], name=v[_NAME_KEY]
                )
            for match in state[_MATCHES_KEY]:
                matches.append(
                    Match(
                        teams=[
                            Team(
                                players=x[_PLAYERS_KEY],
                                points=x[_POINTS_KEY],
                                identifier=x[_IDENTIFIER_KEY],
                            )
                            for x in match[_TEAMS_KEY]
                        ],
                        dt=datetime.datetime.fromisoformat(match[_DT_KEY]),
                    )
                )
        self._team_ratings = team_ratings
        self._player_ratings = player_ratings
        self._matches = matches
        return True

    def save(self, folder: str) -> None:
        """Saves the state to a folder."""
        state_file = os.path.join(folder, self._state_file)
        with open(state_file, "w", encoding="utf8") as handle:
            json.dump(
                {
                    _TEAM_RATINGS_KEY: {
                        k: {
                            _MU_KEY: v.mu,
                            _SIGMA_KEY: v.sigma,
                            _NAME_KEY: v.name,
                        }
                        for k, v in self._team_ratings.items()
                    },
                    _PLAYER_RATINGS_KEY: {
                        k: {
                            _MU_KEY: v.mu,
                            _SIGMA_KEY: v.sigma,
                            _NAME_KEY: v.name,
                        }
                        for k, v in self._player_ratings.items()
                    },
                    _MATCHES_KEY: [
                        {
                            _TEAMS_KEY: [
                                {
                                    _PLAYERS_KEY: y.players,
                                    _POINTS_KEY: y.points,
                                    _IDENTIFIER_KEY: y.identifier,
                                }
                                for y in x.teams
                            ],
                            _DT_KEY: x.dt.isoformat(),
                        }
                        for x in self._matches
                    ],
                },
                handle,
            )

    def reset(self) -> None:
        """Resets the state."""
        self._team_ratings = {}
        self._player_ratings = {}
        self._matches = []
