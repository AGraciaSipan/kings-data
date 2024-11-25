from uuid import UUID

import pytest
from pydantic import ValidationError

from enums import CompetitionFormat, Kingdom, Region
from exceptions.competition_exceptions import (
    DuplicateTeamUUIDException,
    InvalidSplitException,
    RegionMismatchException,
    TeamNotFoundException,
)
from exceptions.shared_exceptions import InvalidUUIDException
from models import Competition, Team


@pytest.fixture
def teams():
    return {
        Team(
            uuid="12345678-1234-5678-1234-567812345678",
            kings_name="Kings Team 1",
            queens_name="Queens Team 1",
            acronym="KT1",
            region=Region.AM,
            first_color="blue",
            second_color="white",
        ),
        Team(
            uuid="23456789-1234-5678-1234-567812345678",
            kings_name="Kings Team 2",
            queens_name="Queens Team 2",
            acronym="KT2",
            region=Region.AM,
            first_color="red",
        ),
    }


@pytest.fixture
def competition(teams):
    return Competition(
        uuid="11111111-1111-1111-1111-111111111111",
        region=Region.AM,
        kingdom=Kingdom.KINGS,
        format=CompetitionFormat.LEAGUE,
        season=2023,
        split=1,
        teams=teams,
    )


def test_competition_initialization(competition, teams):
    assert competition.uuid == UUID("11111111-1111-1111-1111-111111111111")
    assert competition.region == Region.AM.value
    assert competition.kingdom == Kingdom.KINGS.value
    assert competition.format == CompetitionFormat.LEAGUE.value
    assert competition.season == 2023
    assert competition.split == 1
    assert competition.teams == teams


def test_invalid_split_for_league(teams):
    with pytest.raises(InvalidSplitException, match="Split cannot be None for a league competition."):
        Competition(
            uuid="22222222-2222-2222-2222-222222222222",
            region=Region.AM,
            kingdom=Kingdom.QUEENS,
            format=CompetitionFormat.LEAGUE,
            season=2024,
            split=None,
            teams=teams,
        )


def test_invalid_split_for_non_league(teams):
    with pytest.raises(InvalidSplitException, match="Split must be None for non-league competition formats."):
        Competition(
            uuid="33333333-3333-3333-3333-333333333333",
            region=Region.AM,
            kingdom=Kingdom.KINGS,
            format=CompetitionFormat.CUP,
            season=2025,
            split=2,
            teams=teams,
        )


def test_duplicate_team_uuids():
    duplicated_uuid = "12345678-1234-5678-1234-567812345678"
    teams_with_duplicates = {
        Team(
            uuid=duplicated_uuid,
            kings_name="Kings Team 1",
            queens_name="Queens Team 1",
            acronym="KT1",
            region=Region.AM,
            first_color="blue",
        ),
        Team(
            uuid=duplicated_uuid,
            kings_name="Kings Team 2",
            queens_name="Queens Team 2",
            acronym="KT2",
            region=Region.AM,
            first_color="red",
        ),
    }

    with pytest.raises(DuplicateTeamUUIDException) as exc:
        Competition(
            uuid="77777777-7777-7777-7777-777777777777",
            region=Region.AM,
            kingdom=Kingdom.QUEENS,
            format=CompetitionFormat.LEAGUE,
            season=2023,
            split=1,
            teams=teams_with_duplicates,
        )

    assert "The following teams have duplicated UUIDs" in str(exc.value)
    assert "Queens Team 1 (12345678-1234-5678-1234-567812345678)" in str(exc.value)
    assert "Queens Team 2 (12345678-1234-5678-1234-567812345678)" in str(exc.value)


def test_region_mismatch_in_teams():
    teams_with_mismatch = {
        Team(
            uuid="44444444-4444-4444-4444-444444444444",
            kings_name="Kings Team 1",
            queens_name="Queens Team 1",
            acronym="KT1",
            region=Region.ESP,
            first_color="blue",
        ),
        Team(
            uuid="55555555-5555-5555-5555-555555555555",
            kings_name="Kings Team 2",
            queens_name="Queens Team 2",
            acronym="KT2",
            region=Region.AM,
            first_color="red",
        ),
    }

    with pytest.raises(RegionMismatchException) as exc:
        Competition(
            uuid="66666666-6666-6666-6666-666666666666",
            region=Region.AM,
            kingdom=Kingdom.KINGS,
            format=CompetitionFormat.CUP,
            season=2023,
            teams=teams_with_mismatch,
        )

    assert f"regions that do not match the competition's region ({Region.AM.value})" in str(exc.value)
    assert "KT1" in str(exc.value)
    assert "KT2" not in str(exc.value)


def test_get_team_by_uuid(competition):
    team = competition.get_team("12345678-1234-5678-1234-567812345678")
    assert team.uuid_str == "12345678-1234-5678-1234-567812345678"
    assert team.kings_name == "Kings Team 1"
    assert team.acronym == "KT1"


def test_get_team_with_invalid_uuid(competition):
    with pytest.raises(InvalidUUIDException, match="The provided ID 'invalid-uuid-string' is not a valid UUID."):
        competition.get_team("invalid-uuid-string")


def test_get_team_not_found(competition):
    with pytest.raises(
        TeamNotFoundException,
        match="Team with ID '99999999-9999-9999-9999-999999999999' not found in the competition teams.",
    ):
        competition.get_team("99999999-9999-9999-9999-999999999999")


def test_has_team_by_uuid(competition):
    result1 = competition.has_team("12345678-1234-5678-1234-567812345678")
    result2 = competition.has_team("99999999-9999-9999-9999-999999999999")
    assert result1 is True
    assert result2 is False


def test_has_team_with_invalid_uuid(competition):
    with pytest.raises(InvalidUUIDException, match="The provided ID 'invalid-uuid-string' is not a valid UUID."):
        competition.has_team("invalid-uuid-string")


def test_competition_immutability(competition):
    with pytest.raises(ValidationError):
        competition.uuid = UUID("98765432-1234-5678-1234-567812345678")

    with pytest.raises(ValidationError):
        competition.region = Region.ITA

    with pytest.raises(ValidationError):
        competition.kingdom = Kingdom.QUEENS

    with pytest.raises(ValidationError):
        competition.format = CompetitionFormat.CUP

    with pytest.raises(ValidationError):
        competition.season = 2024

    with pytest.raises(ValidationError):
        competition.split = 2

    with pytest.raises(ValidationError):
        competition.teams = set()
