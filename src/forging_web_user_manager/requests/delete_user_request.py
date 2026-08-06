"""Request DTO for deleting a user."""

from dataclasses import dataclass
from uuid import UUID


@dataclass
class DeleteUserRequest:
    user_id: UUID
