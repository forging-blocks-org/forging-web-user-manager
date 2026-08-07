"""Raised when an email is invalid."""

from forging_blocks.foundation.errors import ValueErrorMixin

from forging_web_user_manager.errors.user_error import UserError


class UserEmailInvalidError(ValueErrorMixin, UserError):
    """Raised when an email is invalid."""
