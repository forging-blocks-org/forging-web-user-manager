"""Request DTO for updating a user."""

from dataclasses import dataclass


@dataclass
class UpdateUserRequest:
    user_id: str
    name: str | None = None
    email: str | None = None
