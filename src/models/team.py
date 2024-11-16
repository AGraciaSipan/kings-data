from pydantic import BaseModel, ConfigDict

from enums import Kingdom, Region
from utils import UUIDMixin


class Team(BaseModel, UUIDMixin):
    kings_name: str
    queens_name: str
    acronym: str  # TODO: add regex validation
    region: Region
    first_color: str  # TODO: hex code validation
    second_color: str | None = None

    model_config = ConfigDict(frozen=True, use_enum_values=True)

    def get_team_name(self, kingdom: Kingdom | None = None) -> str:
        if kingdom == Kingdom.QUEENS:
            return self.queens_name

        return self.kings_name
