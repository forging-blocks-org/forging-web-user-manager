"""Tests for InMemoryUserRepository."""

import pytest
from uuid import UUID

from forging_blocks.infrastructure import RepositoryNotFoundError

from forging_web_user_manager.models.email import Email
from forging_web_user_manager.models.user import User
from forging_web_user_manager.repository import InMemoryUserRepository


@pytest.fixture
def repo() -> InMemoryUserRepository:
    """Return a fresh empty repository."""
    return InMemoryUserRepository()


@pytest.fixture
def user() -> User:
    """Return a User with an assigned ID, ready to save."""
    u = User("Alice", Email("alice@example.com"))
    return u


@pytest.mark.asyncio
async def test_save_persists_user(repo: InMemoryUserRepository, user: User):
    """save() persists a user so it can be retrieved by ID."""
    await repo.save(user)

    assert user.id is not None
    retrieved = await repo.get_by_id(user.id)
    assert retrieved is not None
    assert retrieved.id == user.id
    assert retrieved.name == user.name


@pytest.mark.asyncio
async def test_get_by_id_returns_user_for_existing_id(
    repo: InMemoryUserRepository, user: User
):
    """get_by_id() returns the user when the ID exists."""
    await repo.save(user)

    assert user.id is not None
    result = await repo.get_by_id(user.id)

    assert result is not None
    assert result.id == user.id


@pytest.mark.asyncio
async def test_get_by_id_returns_none_for_non_existent_id(
    repo: InMemoryUserRepository,
):
    """get_by_id() returns None when no user has the given ID."""
    result = await repo.get_by_id(UUID("00000000-0000-7000-8000-000000000000"))

    assert result is None


@pytest.mark.asyncio
async def test_delete_by_id_removes_user(repo: InMemoryUserRepository, user: User):
    """delete_by_id() removes the user so it can no longer be retrieved."""
    await repo.save(user)

    assert user.id is not None
    await repo.delete_by_id(user.id)

    retrieved = await repo.get_by_id(user.id)
    assert retrieved is None


@pytest.mark.asyncio
async def test_delete_by_id_raises_repository_not_found_error_for_non_existent_id(
    repo: InMemoryUserRepository,
):
    """delete_by_id() raises RepositoryNotFoundError when the ID does not exist."""
    with pytest.raises(RepositoryNotFoundError):
        await repo.delete_by_id(UUID("00000000-0000-7000-8000-000000000000"))


@pytest.mark.asyncio
async def test_list_all_returns_all_saved_users(
    repo: InMemoryUserRepository,
):
    """list_all() returns every user that has been saved."""
    user1 = User("Alice", Email("alice@example.com"))
    user2 = User("Bob", Email("bob@example.com"))
    await repo.save(user1)
    await repo.save(user2)

    results = await repo.list_all()

    assert len(results) == 2
    ids = {u.id for u in results}
    assert user1.id in ids
    assert user2.id in ids


@pytest.mark.asyncio
async def test_list_all_returns_empty_list_when_no_users(
    repo: InMemoryUserRepository,
):
    """list_all() returns an empty list when nothing has been saved."""
    results = await repo.list_all()

    assert results == []
