"""Tests for the User entity."""

from forging_web_user_manager.models.email import Email
from forging_web_user_manager.models.user import User
from forging_web_user_manager.errors.user_name_empty_error import UserNameEmptyError


def test_create_user_with_name_and_email():
    """User creation stores name and email correctly."""
    email = Email("alice@example.com")
    user = User("Alice", email)

    assert user.name == "Alice"
    assert user.email == email


def test_rename_with_valid_name_returns_ok():
    """rename() with a valid name returns Ok and updates the name."""
    user = User("Alice", Email("alice@example.com"))

    result = user.rename("Bob")

    assert result.is_ok
    assert result.value.name == "Bob"
    assert user.name == "Bob"


def test_rename_with_empty_name_returns_err():
    """rename() with an empty string returns Err(UserNameEmptyError)."""
    user = User("Alice", Email("alice@example.com"))

    result = user.rename("")

    assert result.is_err
    err = result.error
    assert isinstance(err, UserNameEmptyError)
    assert user.name == "Alice"


def test_rename_with_whitespace_only_name_returns_err():
    """rename() with a whitespace-only string returns Err(UserNameEmptyError)."""
    user = User("Alice", Email("alice@example.com"))

    result = user.rename("   ")

    assert result.is_err
    err = result.error
    assert isinstance(err, UserNameEmptyError)
    assert user.name == "Alice"


def test_update_email_with_valid_email_returns_ok():
    """update_email() with a valid Email returns Ok and updates the email."""
    old_email = Email("alice@example.com")
    new_email = Email("alice-new@example.com")
    user = User("Alice", old_email)

    result = user.update_email(new_email)

    assert result.is_ok
    assert result.value.email == new_email
    assert user.email == new_email


def test_assign_id_sets_non_none_non_empty_string():
    """assign_id() sets a non-None, non-empty string id."""
    user = User("Alice", Email("alice@example.com"))

    user.assign_id()

    assert user.id is not None
    assert isinstance(user.id, str)
    assert len(user.id) > 0


def test_assign_id_generates_unique_ids():
    """assign_id() generates unique ids for different users."""
    user1 = User("Alice", Email("alice@example.com"))
    user2 = User("Bob", Email("bob@example.com"))

    user1.assign_id()
    user2.assign_id()

    assert user1.id != user2.id
