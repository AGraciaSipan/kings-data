from typing import Self

from pydantic import (
    BaseModel,
    ConfigDict,
    NonNegativeInt,
    PositiveInt,
    computed_field,
    model_validator,
)

from exceptions.match_exceptions import (
    EqualShootoutGoalsException,
    IdenticalTeamsException,
    MissingShootoutGoalsException,
    NonDrawShootoutGoalsException,
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

    def is_played(self) -> bool:
        return isinstance(self, PlayedMatch)

    def to_played_match(
        self,
        home_goals: NonNegativeInt,
        away_goals: NonNegativeInt,
        home_shootout_goals: NonNegativeInt | None = None,
        away_shootout_goals: NonNegativeInt | None = None,
    ) -> "PlayedMatch":
        return PlayedMatch(
            uuid=self.uuid_str,
            competition=self.competition,
            matchday_round=self.matchday_round,
            home_team=self.home_team,
            away_team=self.away_team,
            home_goals=home_goals,
            away_goals=away_goals,
            home_shootout_goals=home_shootout_goals,
            away_shootout_goals=away_shootout_goals,
        )

    def __str__(self) -> str:
        home_team_name = self.home_team.get_team_name(self.competition.kingdom)
        away_team_name = self.away_team.get_team_name(self.competition.kingdom)

        return f"{home_team_name} - {away_team_name}"


class PlayedMatch(Match):
    home_goals: NonNegativeInt
    away_goals: NonNegativeInt
    home_shootout_goals: NonNegativeInt | None = None
    away_shootout_goals: NonNegativeInt | None = None

    @model_validator(mode="after")
    def validate_shootout_goals(self) -> Self:
        if self.home_goals == self.away_goals:
            if self.home_shootout_goals is None or self.away_shootout_goals is None:
                raise MissingShootoutGoalsException
            if self.home_shootout_goals == self.away_shootout_goals:
                raise EqualShootoutGoalsException
        else:
            if self.home_shootout_goals is not None or self.away_shootout_goals is not None:
                raise NonDrawShootoutGoalsException

        return self

    @computed_field
    @property
    def regular_time_winner(self) -> Team | None:
        if self.home_goals > self.away_goals:
            return self.home_team
        elif self.away_goals > self.home_goals:
            return self.away_team
        return None

    @computed_field
    @property
    def winner(self) -> Team:
        if self.regular_time_winner:
            return self.regular_time_winner

        if self.home_shootout_goals > self.away_shootout_goals:
            return self.home_team
        else:
            return self.away_team

    def __str__(self) -> str:
        home_team_name = self.home_team.get_team_name(self.competition.kingdom)
        away_team_name = self.away_team.get_team_name(self.competition.kingdom)
        home_goals = self.home_goals
        away_goals = self.away_goals

        if self.regular_time_winner:
            return f"{home_team_name} {home_goals} - {away_goals} {away_team_name}"

        return f"{home_team_name} {home_goals} ({self.home_shootout_goals}) - ({self.away_shootout_goals}) {away_goals} {away_team_name}"  # noqa: E501
