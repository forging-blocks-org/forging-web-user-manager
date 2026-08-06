"""Tests for RegisterUserUseCase."""

from uuid import UUID

import pytest

from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.errors.user_name_empty_error import UserNameEmptyError
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.responses.user_response import UserResponse
from forging_web_user_manager.requests.register_user_request import RegisterUserRequest
from forging_web_user_manager.services.register_user_use_case import RegisterUserUseCase


@pytest.fixture
def repo() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def use_case(repo: InMemoryUserRepository) -> RegisterUserUseCase:
    return RegisterUserUseCase(repo)


@pytest.mark.asyncio
async def test_register_user_with_valid_name_and_email_returns_ok_with_user(
    use_case: RegisterUserUseCase,
) -> None:
    request = RegisterUserRequest(name="Alice", email="alice@example.com")

    result = await use_case.execute(request)

    assert result.is_ok
    user = result.value
    assert isinstance(user, UserResponse)
    assert user.name == "Alice"
    assert user.email == "alice@example.com"


@pytest.mark.asyncio
async def test_register_user_with_invalid_email_no_at_returns_err(
    use_case: RegisterUserUseCase,
) -> None:
    request = RegisterUserRequest(name="Alice", email="bademail")

    result = await use_case.execute(request)

    assert result.is_err
    assert isinstance(result.error, UserError)
    assert result.error.message.value == "Invalid email format"


@pytest.mark.asyncio
async def test_register_user_with_empty_name_returns_err(
    use_case: RegisterUserUseCase,
) -> None:
    request = RegisterUserRequest(name="", email="alice@example.com")

    result = await use_case.execute(request)

    assert result.is_err
    assert isinstance(result.error, UserNameEmptyError)
    assert result.error.message.value == "User name cannot be empty"


@pytest.mark.asyncio
async def test_registered_user_has_assigned_id(
    use_case: RegisterUserUseCase,
) -> None:
    request = RegisterUserRequest(name="Alice", email="alice@example.com")

    result = await use_case.execute(request)

    assert result.is_ok
    user = result.value
    assert isinstance(user, UserResponse)
    assert user.id is not None
    assert isinstance(user.id, UUID)
