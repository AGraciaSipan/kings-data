import pytest

from enums import CompetitionFormat, Kingdom, Region
from models.competition import Competition
from models.team import Team


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
