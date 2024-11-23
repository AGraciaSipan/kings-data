from enums import Region


class CompetitionException(Exception):
    pass


class DuplicateTeamUUIDException(CompetitionException):
    def __init__(self, duplicate_info: list[str]):
        self.message = f"The following teams have duplicated UUIDs: {', '.join(duplicate_info)}."
        super().__init__(self.message)


class InvalidSplitException(CompetitionException):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class RegionMismatchException(CompetitionException):
    def __init__(self, region: Region, invalid_teams: list[str]):
        self.message = (
            f"The following teams have regions that do not match the competition's region ({region}): "
            f"{', '.join(invalid_teams)}."
        )
        super().__init__(self.message)


class TeamNotFoundException(CompetitionException):
    def __init__(self, team_id: str):
        self.message = f"Team with ID '{team_id}' not found in the competition teams."
        super().__init__(self.message)
