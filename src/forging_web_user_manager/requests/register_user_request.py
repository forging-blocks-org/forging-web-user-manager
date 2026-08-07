"""Request DTO for registering a user."""

from dataclasses import dataclass


@dataclass
class RegisterUserRequest:
    name: str
    email: str
