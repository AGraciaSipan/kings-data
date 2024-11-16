from uuid import UUID

from pydantic import field_validator


class UUIDMixin:
    uuid: str

    @field_validator("uuid")
    @classmethod
    def validate_uuid(cls, v) -> UUID:
        if isinstance(v, str):
            try:
                return UUID(v)
            except ValueError:
                raise ValueError(f"Invalid UUID string: {v}")
        elif isinstance(v, UUID):
            return v
        else:
            raise ValueError(f"Invalid UUID format: {v}")

    @property
    def uuid_str(self) -> str:
        return str(self.uuid)
