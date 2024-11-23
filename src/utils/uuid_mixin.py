from uuid import UUID

from pydantic import field_validator

from exceptions.shared_exceptions import InvalidUUIDException


class UUIDMixin:
    uuid: str

    @field_validator("uuid")
    @classmethod
    def validate_uuid(cls, v) -> UUID:
        try:
            return UUID(v)
        except ValueError:
            raise InvalidUUIDException(v)

    @property
    def uuid_str(self) -> str:
        return str(self.uuid)
