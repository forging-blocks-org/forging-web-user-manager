"""Tests for CreateUserUseCase."""

import pytest

from forging_web_user_manager.errors.user_error import UserError
from forging_web_user_manager.errors.user_name_empty_error import UserNameEmptyError
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.responses.user_response import UserResponse
from forging_web_user_manager.requests.create_user_request import CreateUserRequest
from forging_web_user_manager.services.create_user_use_case import CreateUserUseCase


@pytest.fixture
def repo() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def use_case(repo: InMemoryUserRepository) -> CreateUserUseCase:
    return CreateUserUseCase(repo)


@pytest.mark.asyncio
async def test_create_user_with_valid_name_and_email_returns_ok_with_user(
    use_case: CreateUserUseCase,
) -> None:
    request = CreateUserRequest(name="Alice", email="alice@example.com")

    result = await use_case.execute(request)

    assert result.is_ok
    user = result.value
    assert isinstance(user, UserResponse)
    assert user.name == "Alice"
    assert user.email == "alice@example.com"


@pytest.mark.asyncio
async def test_create_user_with_invalid_email_no_at_returns_err(
    use_case: CreateUserUseCase,
) -> None:
    request = CreateUserRequest(name="Alice", email="bademail")

    result = await use_case.execute(request)

    assert result.is_err
    assert isinstance(result.error, UserError)
    assert result.error.message.value == "Invalid email format"


@pytest.mark.asyncio
async def test_create_user_with_empty_name_returns_err(
    use_case: CreateUserUseCase,
) -> None:
    request = CreateUserRequest(name="", email="alice@example.com")

    result = await use_case.execute(request)

    assert result.is_err
    assert isinstance(result.error, UserNameEmptyError)
    assert result.error.message.value == "User name cannot be empty"


@pytest.mark.asyncio
async def test_created_user_has_assigned_id(
    use_case: CreateUserUseCase,
) -> None:
    request = CreateUserRequest(name="Alice", email="alice@example.com")

    result = await use_case.execute(request)

    assert result.is_ok
    user = result.value
    assert isinstance(user, UserResponse)
    assert user.id is not None
    assert len(user.id) == 32  # uuid4().hex produces 32 hex chars
