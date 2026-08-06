"""In-memory user repository backed by forging-blocks InMemoryRepository."""

from forging_blocks.infrastructure import InMemoryRepository

from forging_web_user_manager.models.user import User


class InMemoryUserRepository(InMemoryRepository[User, str]):
    """In-memory repository for User aggregates, keyed by string ID."""
