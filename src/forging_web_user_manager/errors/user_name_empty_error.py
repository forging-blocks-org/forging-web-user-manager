"""Raised when a user name is empty."""

from forging_blocks.foundation.errors import ValueErrorMixin

from forging_web_user_manager.errors.user_error import UserError


class UserNameEmptyError(ValueErrorMixin, UserError):
    """Raised when a user name is empty."""
