"""Request DTO for deleting a user."""

from dataclasses import dataclass


@dataclass
class DeleteUserRequest:
    user_id: str
