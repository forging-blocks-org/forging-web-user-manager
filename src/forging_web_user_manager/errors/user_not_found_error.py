"""Raised when a requested user does not exist."""

from forging_blocks.foundation.errors import RuntimeErrorMixin

from forging_web_user_manager.errors.user_error import UserError


class UserNotFoundError(RuntimeErrorMixin, UserError):
    """Raised when a requested user does not exist."""
