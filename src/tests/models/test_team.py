from uuid import UUID

import pytest
from pydantic import ValidationError

from enums import Kingdom, Region
from models import Team


@pytest.fixture
def team():
    return Team(
        uuid="12345678-1234-5678-1234-567812345678",
        kings_name="Kings Team",
        queens_name="Queens Team",
        acronym="ABC",
        region=Region.AM,
        first_color="blue",
        second_color="white",
    )


@pytest.fixture
def team_factory():
    def create_team(
        uuid,
        kings_name="Kings Team",
        queens_name="Queens Team",
        acronym="ABC",
        region=Region.AM,
        first_color="blue",
        second_color="white",
    ):
        return Team(
            uuid=uuid,
            kings_name=kings_name,
            queens_name=queens_name,
            acronym=acronym,
            region=region,
            first_color=first_color,
            second_color=second_color,
        )

    return create_team


def test_uuid_conversion(team):
    assert isinstance(team.uuid, UUID)
    assert str(team.uuid) == "12345678-1234-5678-1234-567812345678"


def test_invalid_uuid_string():
    with pytest.raises(ValueError, match="Invalid UUID string"):
        Team(
            uuid="invalid-uuid-string",
            kings_name="Kings Team",
            queens_name="Queens Team",
            acronym="ABC",
            region=Region.AM,
            first_color="blue",
            second_color="white",
        )


def test_team_initialization(team):
    assert team.uuid == UUID("12345678-1234-5678-1234-567812345678")
    assert team.kings_name == "Kings Team"
    assert team.queens_name == "Queens Team"
    assert team.acronym == "ABC"
    assert team.region == Region.AM.value
    assert team.first_color == "blue"
    assert team.second_color == "white"


def test_uuid_str_property(team):
    uuid_str = team.uuid_str

    assert uuid_str == "12345678-1234-5678-1234-567812345678"


def test_get_team_name_default(team):
    team_name = team.get_team_name()

    assert team_name == "Kings Team"


def test_get_team_name_kings(team):
    team_name = team.get_team_name(Kingdom.KINGS)

    assert team_name == "Kings Team"


def test_get_team_name_queens(team):
    team_name = team.get_team_name(Kingdom.QUEENS)

    assert team_name == "Queens Team"


def test_team_immutability(team):
    with pytest.raises(ValidationError):
        team.uuid = UUID("98765432-1234-5678-1234-567812345678")

    with pytest.raises(ValidationError):
        team.kings_name = "New Kings Team"

    with pytest.raises(ValidationError):
        team.queens_name = "New Queens Team"

    with pytest.raises(ValidationError):
        team.acronym = "NEW"

    with pytest.raises(ValidationError):
        team.region = Region.ITA

    with pytest.raises(ValidationError):
        team.first_color = "red"

    with pytest.raises(ValidationError):
        team.second_color = "green"