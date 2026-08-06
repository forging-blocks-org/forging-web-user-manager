"""Request DTO for getting a user by ID."""

from dataclasses import dataclass


@dataclass
class GetUserRequest:
    user_id: str
