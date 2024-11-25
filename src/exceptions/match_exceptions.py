class MatchException(Exception):
    pass


class IdenticalTeamsException(Exception):
    def __init__(self, team_name: str):
        super().__init__(f"Home team and away team cannot be the same: '{team_name}'.")


class TeamNotInCompetitionException(MatchException):
    def __init__(self, team_name: str):
        self.message = f"Team '{team_name}' is not listed in the provided competition."
        super().__init__(self.message)
