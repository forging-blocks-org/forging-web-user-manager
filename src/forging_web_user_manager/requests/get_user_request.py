"""Request DTO for getting a user by ID."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class GetUserRequest:
    user_id: UUID
