class MatchException(Exception):
    pass


class IdenticalTeamsException(Exception):
    def __init__(self, team_name: str):
        super().__init__(f"Home team and away team cannot be the same: '{team_name}'.")


class TeamNotInCompetitionException(MatchException):
    def __init__(self, team_name: str):
        self.message = f"Team '{team_name}' is not listed in the provided competition."
        super().__init__(self.message)


class PlayedMatchException(MatchException):
    pass


class MissingShootoutGoalsException(PlayedMatchException):
    def __init__(self):
        self.message = "Shootout goals must be provided if the match is a draw in regular time."
        super().__init__(self.message)


class EqualShootoutGoalsException(PlayedMatchException):
    def __init__(self):
        self.message = "Shootout goals cannot be equal."
        super().__init__(self.message)


class NonDrawShootoutGoalsException(PlayedMatchException):
    def __init__(self):
        self.message = "Shootout goals must be None for a non-draw match."
        super().__init__(self.message)
