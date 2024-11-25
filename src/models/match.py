from typing import Self

from pydantic import BaseModel, ConfigDict, PositiveInt, model_validator

from exceptions.match_exceptions import (
    IdenticalTeamsException,
    TeamNotInCompetitionException,
)
from models.competition import Competition
from models.team import Team
from utils import UUIDMixin


class Match(BaseModel, UUIDMixin):
    competition: Competition
    matchday_round: PositiveInt
    home_team: Team
    away_team: Team

    model_config = ConfigDict(frozen=True)

    @model_validator(mode="after")
    def validate_teams_in_competition(self) -> Self:
        if not self.competition.has_team(self.home_team.uuid_str):
            raise TeamNotInCompetitionException(self.home_team.get_team_name(self.competition.kingdom))
        if not self.competition.has_team(self.away_team.uuid_str):
            raise TeamNotInCompetitionException(self.away_team.get_team_name(self.competition.kingdom))

        return self

    @model_validator(mode="after")
    def validate_different_teams(self) -> Self:
        if self.home_team == self.away_team:
            raise IdenticalTeamsException(self.home_team.get_team_name(self.competition.kingdom))

        return self

    def __str__(self) -> str:
        home_team_name = self.home_team.get_team_name(self.competition.kingdom)
        away_team_name = self.away_team.get_team_name(self.competition.kingdom)

        return f"{home_team_name} - {away_team_name}"
