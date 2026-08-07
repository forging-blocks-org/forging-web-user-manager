"""A user aggregate root identified by a UUID."""

from os import urandom
from time import time
from typing import Self
from uuid import UUID

from forging_blocks.domain.aggregate_root.aggregate_root import AggregateRoot
from forging_blocks.domain.messages.event import Event
from forging_blocks.foundation import Err, Ok, Result

from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.errors.user_name_empty_error import UserNameEmptyError
from forging_web_user_manager.models.user_registered import (
    UserRegistered,
    UserRegisteredPayload,
)
from forging_web_user_manager.models.email import Email


def _uuid7() -> UUID:
    """Generate a UUIDv7 per RFC 9562.

    48-bit Unix millisecond timestamp in the most significant bits,
    74 cryptographically random bits in the remaining positions.
    """
    timestamp_ms = int(time() * 1000) & 0xFFFFFFFFFFFF
    rand_bytes = urandom(16)
    uuid_bytes = bytearray(16)
    uuid_bytes[0:6] = timestamp_ms.to_bytes(6, "big")
    uuid_bytes[6] = 0x70 | (rand_bytes[6] & 0x0F)
    uuid_bytes[7] = rand_bytes[7]
    uuid_bytes[8] = 0x80 | (rand_bytes[8] & 0x3F)
    uuid_bytes[9:16] = rand_bytes[9:16]
    return UUID(bytes=bytes(uuid_bytes))


class User(AggregateRoot[UUID, UserRegisteredPayload]):
    """A user aggregate root identified by a UUID."""

    def __init__(self, name: str, email: Email) -> None:
        user_id = _uuid7()
        super().__init__(user_id)
        self.apply(UserRegistered(user_id=user_id, name=name, email=email.value))

    def _handle(self, event: Event[UserRegisteredPayload]) -> None:
        """Mutate aggregate state in response to a domain event."""
        if isinstance(event, UserRegistered):
            self.name = event.name
            self.email = Email(event.email)

    def rename(self, new_name: str) -> Result[Self, UserError]:
        """Rename the user. Returns Err if name is empty."""
        if not new_name.strip():
            return Err(UserNameEmptyError.from_string("User name cannot be empty"))
        self.name = new_name
        return Ok(self)

    def update_email(self, new_email: Email) -> Result[Self, UserError]:
        """Update the user's email. Validation is handled by Email constructor."""
        self.email = new_email
        return Ok(self)
