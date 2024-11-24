from typing import Self
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, PositiveInt, model_validator

from enums import CompetitionFormat, Kingdom, Region
from exceptions.competition_exceptions import (
    DuplicateTeamUUIDException,
    InvalidSplitException,
    RegionMismatchException,
    TeamNotFoundException,
)
from exceptions.shared_exceptions import InvalidUUIDException
from models.team import Team
from utils import UUIDMixin


class Competition(BaseModel, UUIDMixin):
    region: Region
    kingdom: Kingdom
    format: CompetitionFormat
    season: int = Field(ge=2023, le=2025)
    split: PositiveInt | None = None
    teams: frozenset[Team]

    model_config = ConfigDict(frozen=True, use_enum_values=True)

    _teams_dict: dict[UUID, Team] = {}

    def __init__(self, **data):
        super().__init__(**data)
        self._teams_dict = {team.uuid: team for team in self.teams}

    @model_validator(mode="after")
    def validate_split(self) -> Self:
        if self.split is None and self.format == CompetitionFormat.LEAGUE.value:
            raise InvalidSplitException("Split cannot be None for a league competition.")
        if self.split is not None and self.format != CompetitionFormat.LEAGUE.value:
            raise InvalidSplitException("Split must be None for non-league competition formats.")

        return self

    @model_validator(mode="after")
    def validate_unique_team_uuids(self) -> Self:
        seen_uuids = {}
        duplicate_teams = []

        for team in self.teams:
            if team.uuid in seen_uuids:
                if seen_uuids[team.uuid] not in duplicate_teams:
                    duplicate_teams.append(seen_uuids[team.uuid])
                duplicate_teams.append(team)
            else:
                seen_uuids[team.uuid] = team

        if duplicate_teams:
            duplicate_info = [f"{team.get_team_name(self.kingdom)} ({team.uuid})" for team in duplicate_teams]
            raise DuplicateTeamUUIDException(duplicate_info)

        return self

    @model_validator(mode="after")
    def validate_teams_region(self) -> Self:
        invalid_teams = [team.acronym for team in self.teams if team.region != self.region]
        if invalid_teams:
            raise RegionMismatchException(self.region, invalid_teams)

        return self

    def get_team(self, team_uuid_str: str) -> Team:
        try:
            team_uuid = UUID(team_uuid_str)
        except ValueError:
            raise InvalidUUIDException(team_uuid_str)

        team = self._teams_dict.get(team_uuid)
        if not team:
            raise TeamNotFoundException(team_uuid_str)

        return team
