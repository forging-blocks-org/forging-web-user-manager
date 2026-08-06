"""Tests for the Email value object."""

import pytest

from forging_web_user_manager.models.email import Email


def test_create_email_with_valid_address():
    """Email creation with a valid address succeeds."""
    email = Email("alice@example.com")

    assert email.value == "alice@example.com"


def test_create_email_without_at_symbol_raises_value_error():
    """Email creation without '@' raises ValueError."""
    with pytest.raises(ValueError, match="Invalid email format"):
        Email("not-an-email")


def test_email_value_property_returns_raw_string():
    """Email.value returns the raw string passed at construction."""
    raw = "user@domain.com"
    email = Email(raw)

    assert email.value == raw


def test_emails_with_same_value_are_equal():
    """Two Email instances with the same value are equal."""
    email1 = Email("a@b.com")
    email2 = Email("a@b.com")

    assert email1 == email2


def test_emails_with_different_values_are_not_equal():
    """Two Email instances with different values are not equal."""
    email1 = Email("a@b.com")
    email2 = Email("c@d.com")

    assert email1 != email2
