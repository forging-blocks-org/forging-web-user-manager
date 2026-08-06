"""Email address value object with basic format validation."""

from forging_blocks.domain.value_object import ValueObject


class Email(ValueObject[str]):
    """Email address value object with basic format validation."""

    __slots__ = ("_value",)

    def __init__(self, value: str) -> None:
        if "@" not in value:
            raise ValueError("Invalid email format")
        object.__setattr__(self, "_value", value)

    @property
    def value(self) -> str:
        """The raw email string."""
        return self._value
