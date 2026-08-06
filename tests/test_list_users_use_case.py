"""Tests for ListUsersUseCase."""

from typing import cast
import pytest


from forging_web_user_manager.models.email import Email
from forging_web_user_manager.models.user import User
from forging_web_user_manager.repository import InMemoryUserRepository
from forging_web_user_manager.responses.user_response import UserResponse
from forging_web_user_manager.services.list_users_use_case import ListUsersUseCase


@pytest.fixture
def repo() -> InMemoryUserRepository:
    return InMemoryUserRepository()


@pytest.fixture
def use_case(repo: InMemoryUserRepository) -> ListUsersUseCase:
    return ListUsersUseCase(repo)


@pytest.mark.asyncio
async def test_list_users_when_empty_returns_ok_with_empty_list(
    use_case: ListUsersUseCase,
) -> None:
    result = await use_case.execute()

    assert result.is_ok
    assert result.value == []


@pytest.mark.asyncio
async def test_list_users_after_creating_users_returns_all_users(
    repo: InMemoryUserRepository,
    use_case: ListUsersUseCase,
) -> None:
    alice = User(name="Alice", email=Email("alice@example.com"))
    alice.assign_id()
    await repo.save(alice)

    bob = User(name="Bob", email=Email("bob@example.com"))
    bob.assign_id()
    await repo.save(bob)

    result = await use_case.execute()

    assert result.is_ok
    users = result.value
    assert isinstance(users, list)
    assert len(users) == 2
    assert all(isinstance(u, UserResponse) for u in users)
    assert any(u.id == cast(str, alice.id) for u in users)
    assert any(u.id == cast(str, bob.id) for u in users)
