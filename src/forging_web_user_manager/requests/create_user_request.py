"""Request DTO for creating a user."""

from dataclasses import dataclass


@dataclass
class CreateUserRequest:
    name: str
    email: str
