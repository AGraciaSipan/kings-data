from uuid import UUID

from pydantic import field_validator

from exceptions.shared_exceptions import InvalidUUIDException


class UUIDMixin:
    uuid: str

    @field_validator("uuid")
    @classmethod
    def validate_uuid_field(cls, v) -> UUID:
        return cls.validate_uuid(v)

    @staticmethod
    def validate_uuid(value: str) -> UUID:
        try:
            return UUID(value)
        except ValueError:
            raise InvalidUUIDException(value)

    @property
    def uuid_str(self) -> str:
        return str(self.uuid)
