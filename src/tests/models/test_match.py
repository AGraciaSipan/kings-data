from uuid import UUID

import pytest
from pydantic import ValidationError

from enums import Region
from exceptions.match_exceptions import (
    IdenticalTeamsException,
    TeamNotInCompetitionException,
)
from models import Match, Team


@pytest.fixture
def valid_match(competition, teams):
    team_1 = next(team for team in teams if team.uuid_str == "12345678-1234-5678-1234-567812345678")
    team_2 = next(team for team in teams if team.uuid_str == "23456789-1234-5678-1234-567812345678")
    return Match(
        uuid="55555555-5555-5555-5555-555555555555",
        competition=competition,
        matchday_round=1,
        home_team=team_1,
        away_team=team_2,
    )


def test_match_initialization(valid_match):
    assert valid_match.uuid == UUID("55555555-5555-5555-5555-555555555555")
    assert valid_match.matchday_round == 1
    assert valid_match.home_team.acronym == "KT1"
    assert valid_match.away_team.acronym == "KT2"


def test_identical_teams_exception(competition, teams):
    team_1 = next(team for team in teams if team.uuid_str == "12345678-1234-5678-1234-567812345678")
    with pytest.raises(IdenticalTeamsException, match="Home team and away team cannot be the same: 'Kings Team 1'"):
        Match(
            uuid="66666666-6666-6666-6666-666666666666",
            competition=competition,
            matchday_round=1,
            home_team=team_1,
            away_team=team_1,
        )


def test_team_not_in_competition_exception(competition):
    external_team = Team(
        uuid="99999999-9999-9999-9999-999999999999",
        kings_name="External Team",
        queens_name="External Team",
        acronym="ET",
        region=Region.AM,
        first_color="green",
    )
    with pytest.raises(
        TeamNotInCompetitionException, match="Team 'External Team' is not listed in the provided competition."
    ):
        Match(
            uuid="77777777-7777-7777-7777-777777777777",
            competition=competition,
            matchday_round=1,
            home_team=external_team,
            away_team=external_team,
        )


def test_invalid_uuid_in_match_creation(competition, teams):
    team_1 = next(team for team in teams if team.uuid_str == "12345678-1234-5678-1234-567812345678")
    team_2 = next(team for team in teams if team.uuid_str == "23456789-1234-5678-1234-567812345678")
    with pytest.raises(ValueError, match="The provided ID 'invalid-uuid-string' is not a valid UUID."):
        Match(
            uuid="invalid-uuid-string",
            competition=competition,
            matchday_round=1,
            home_team=team_1,
            away_team=team_2,
        )


def test_match_str_representation(valid_match):
    expected_str = "Kings Team 1 - Kings Team 2"
    assert str(valid_match) == expected_str


def test_match_immutability(valid_match):
    with pytest.raises(ValidationError):
        valid_match.uuid = UUID("98765432-1234-5678-1234-567812345678")

    with pytest.raises(ValidationError):
        valid_match.matchday_round = 2

    with pytest.raises(ValidationError):
        valid_match.home_team = valid_match.away_team

    with pytest.raises(ValidationError):
        valid_match.away_team = valid_match.home_team
