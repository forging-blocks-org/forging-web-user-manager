"""A user aggregate root identified by a string ID."""

from typing import Self
from uuid import uuid4

from forging_blocks.domain.entity import Entity
from forging_blocks.foundation import Ok, Err, Result

from forging_web_user_manager.models.email import Email
from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.errors.user_name_empty_error import UserNameEmptyError


class User(Entity[str]):
    """A user aggregate root identified by a string ID."""

    def __init__(self, name: str, email: Email) -> None:
        super().__init__(None)
        self.name = name
        self.email = email

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

    def assign_id(self) -> None:
        """Assign a new UUID-based ID to this draft entity."""
        self._id = uuid4().hex
