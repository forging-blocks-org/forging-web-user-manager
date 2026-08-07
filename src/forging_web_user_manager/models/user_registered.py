"""UserRegistered domain event — emitted when a new user is registered."""

from dataclasses import dataclass
from uuid import UUID

from forging_blocks.domain.messages.event import Event
from forging_blocks.domain.messages.message._metadata import MessageMetadata


@dataclass
class UserRegisteredPayload:
    """Payload for the UserRegistered event."""

    user_id: UUID
    name: str
    email: str


class UserRegistered(Event[UserRegisteredPayload]):
    """Emitted when a new user is registered in the system."""

    def __init__(self, user_id: UUID, name: str, email: str) -> None:
        super().__init__()
        self._user_id = user_id
        self._name = name
        self._email = email

    @property
    def user_id(self) -> UUID:
        """The registered user's unique identifier."""
        return self._user_id

    @property
    def name(self) -> str:
        """The registered user's name."""
        return self._name

    @property
    def email(self) -> str:
        """The registered user's email address."""
        return self._email

    @property
    def _payload(self) -> UserRegisteredPayload:
        """Return the event-specific payload data."""
        return UserRegisteredPayload(
            user_id=self._user_id,
            name=self._name,
            email=self._email,
        )

    @classmethod
    def from_payload_fields(
        cls, data: UserRegisteredPayload, metadata: MessageMetadata
    ) -> "UserRegistered":
        """Reconstruct a UserRegistered event from payload fields and metadata."""
        return cls(
            user_id=data.user_id,
            name=data.name,
            email=data.email,
        )

    @property
    def value(self) -> UserRegisteredPayload:
        """Return the raw event payload."""
        return self._payload
