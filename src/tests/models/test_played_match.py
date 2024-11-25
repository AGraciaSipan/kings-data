from uuid import UUID

import pytest
from pydantic import ValidationError

from exceptions.match_exceptions import (
    EqualShootoutGoalsException,
    MissingShootoutGoalsException,
    NonDrawShootoutGoalsException,
)
from models import PlayedMatch


@pytest.fixture
def played_match_factory(competition, teams):
    team1 = next(team for team in teams if team.acronym == "KT1")
    team2 = next(team for team in teams if team.acronym == "KT2")

    def create_played_match(**overrides):
        defaults = {
            "uuid": "22222222-2222-2222-2222-222222222222",
            "competition": competition,
            "matchday_round": 1,
            "home_team": team1,
            "away_team": team2,
            "home_goals": 0,
            "away_goals": 0,
            "home_shootout_goals": None,
            "away_shootout_goals": None,
        }
        defaults.update(overrides)
        return PlayedMatch(**defaults)

    return create_played_match


def test_regular_time_winner(played_match_factory):
    match = played_match_factory(home_goals=3, away_goals=2)
    assert match.regular_time_winner == match.home_team

    match = played_match_factory(home_goals=2, away_goals=3)
    assert match.regular_time_winner == match.away_team

    match = played_match_factory(home_goals=2, away_goals=2, home_shootout_goals=4, away_shootout_goals=3)
    assert match.regular_time_winner is None


def test_winner(played_match_factory):
    match = played_match_factory(home_goals=4, away_goals=1)
    assert match.winner == match.home_team

    match = played_match_factory(home_goals=1, away_goals=4)
    assert match.winner == match.away_team

    match = played_match_factory(home_goals=0, away_goals=0, home_shootout_goals=4, away_shootout_goals=3)
    assert match.winner == match.home_team


def test_missing_shootout_goals_error(played_match_factory):
    with pytest.raises(
        MissingShootoutGoalsException, match="Shootout goals must be provided if the match is a draw in regular time."
    ):
        played_match_factory(home_goals=2, away_goals=2)


def test_equal_shootout_goals_error(played_match_factory):
    with pytest.raises(EqualShootoutGoalsException, match="Shootout goals cannot be equal."):
        played_match_factory(home_goals=2, away_goals=2, home_shootout_goals=3, away_shootout_goals=3)


def test_non_draw_shootout_goals_error(played_match_factory):
    with pytest.raises(NonDrawShootoutGoalsException, match="Shootout goals must be None for a non-draw match."):
        played_match_factory(home_goals=3, away_goals=2, home_shootout_goals=1, away_shootout_goals=0)


def test_is_played(played_match_factory):
    match = played_match_factory(home_goals=2, away_goals=0)
    assert match.is_played()


def test_string_representation(played_match_factory):
    match = played_match_factory(home_goals=2, away_goals=2, home_shootout_goals=4, away_shootout_goals=3)
    assert str(match) == "Kings Team 1 2 (4) - (3) 2 Kings Team 2"

    match = played_match_factory(home_goals=3, away_goals=2)
    assert str(match) == "Kings Team 1 3 - 2 Kings Team 2"

    match = played_match_factory(home_goals=2, away_goals=3)
    assert str(match) == "Kings Team 1 2 - 3 Kings Team 2"


def test_played_match_immutability(played_match_factory):
    match = played_match_factory(home_goals=3, away_goals=2)
    with pytest.raises(ValidationError):
        match.uuid = UUID("98765432-1234-5678-1234-567812345678")

    with pytest.raises(ValidationError):
        match.matchday_round = 2

    with pytest.raises(ValidationError):
        match.home_team = match.away_team

    with pytest.raises(ValidationError):
        match.away_team = match.home_team

    with pytest.raises(ValidationError):
        match.home_goals = 5

    with pytest.raises(ValidationError):
        match.away_goals = 5

    with pytest.raises(ValidationError):
        match.home_shootout_goals = 10

    with pytest.raises(ValidationError):
        match.away_shootout_goals = 10
