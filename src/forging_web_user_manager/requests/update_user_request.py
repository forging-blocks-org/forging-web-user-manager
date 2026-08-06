"""Request DTO for updating a user."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class UpdateUserRequest:
    user_id: UUID
    name: str | None = None
    email: str | None = None
