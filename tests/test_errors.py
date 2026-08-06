"""Tests for the User error hierarchy."""

import pytest

from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.errors.user_email_invalid_error import UserEmailInvalidError
from forging_web_user_manager.errors.user_name_empty_error import UserNameEmptyError
from forging_web_user_manager.errors.user_not_found_error import UserNotFoundError


def test_user_error_from_string_creates_error_with_correct_message():
    """UserError.from_string() creates an error with the given message."""
    error = UserError.from_string("Something went wrong")

    assert error.message.value == "Something went wrong"


def test_user_email_invalid_error_is_catchable_as_value_error():
    """UserEmailInvalidError is catchable as ValueError via ValueErrorMixin."""
    error = UserEmailInvalidError.from_string("Bad email")

    with pytest.raises(ValueError):
        raise error


def test_user_name_empty_error_is_catchable_as_value_error():
    """UserNameEmptyError is catchable as ValueError via ValueErrorMixin."""
    error = UserNameEmptyError.from_string("Name is empty")

    with pytest.raises(ValueError):
        raise error


def test_user_not_found_error_is_catchable_as_runtime_error():
    """UserNotFoundError is catchable as RuntimeError via RuntimeErrorMixin."""
    error = UserNotFoundError.from_string("User not found")

    with pytest.raises(RuntimeError):
        raise error


def test_all_errors_are_catchable_as_user_error():
    """All concrete errors are catchable as the base UserError."""
    errors = [
        UserEmailInvalidError.from_string("e1"),
        UserNameEmptyError.from_string("e2"),
        UserNotFoundError.from_string("e3"),
    ]

    for error in errors:
        with pytest.raises(UserError):
            raise error


def test_error_message_is_accessible_via_message_value():
    """Error message is accessible via .message.value."""
    msg = "User name cannot be empty"
    error = UserNameEmptyError.from_string(msg)

    assert error.message.value == msg
