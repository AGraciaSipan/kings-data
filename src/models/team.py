from pydantic import BaseModel, ConfigDict, Field
from pydantic_extra_types.color import Color

from enums import Kingdom, Region
from exceptions.enum_exceptions import InvalidEnumValueError
from utils import UUIDMixin


class Team(BaseModel, UUIDMixin):
    kings_name: str
    queens_name: str
    acronym: str = Field(pattern=r"^[A-Z0-9]{2,3}$")
    region: Region
    first_color: Color
    second_color: Color | None = None

    model_config = ConfigDict(frozen=True, use_enum_values=True)

    def get_team_name(self, kingdom: str | Kingdom | None = None) -> str:
        if kingdom:
            try:
                kingdom_enum = Kingdom(kingdom)
            except ValueError:
                raise InvalidEnumValueError(Kingdom, kingdom)

            if kingdom_enum == Kingdom.QUEENS:
                return self.queens_name

        return self.kings_name
