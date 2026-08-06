"""Tests for UserResponse — Pydantic model and from_dto factory."""

import pytest
from pydantic import ValidationError

from forging_web_user_manager.responses.user_response import UserResponse as UserResponseDTO
from forging_web_user_manager.schemas.user_response import UserResponse


class TestUserResponseFromDto:
    """Tests for UserResponse.from_dto() factory method."""

    def test_maps_dto_fields_correctly(self):
        """from_dto() should map id, name, and email from a response DTO."""
        dto = UserResponseDTO(id="abc123", name="Alice", email="alice@example.com")

        response = UserResponse.from_dto(dto)

        assert response.id == "abc123"
        assert response.name == "Alice"
        assert response.email == "alice@example.com"

    def test_maps_dto_with_different_email(self):
        """from_dto() should correctly map a DTO with a different email."""
        dto = UserResponseDTO(id="def456", name="Bob", email="bob@test.org")

        response = UserResponse.from_dto(dto)

        assert response.name == "Bob"
        assert response.email == "bob@test.org"


class TestUserResponseModel:
    """Tests for UserResponse as a Pydantic model."""

    def test_valid_pydantic_model_construction(self):
        """UserResponse should be constructable as a valid Pydantic model."""
        response = UserResponse(id="abc123", name="Alice", email="alice@example.com")

        assert response.id == "abc123"
        assert response.name == "Alice"
        assert response.email == "alice@example.com"

    def test_model_dump_returns_dict(self):
        """UserResponse.model_dump() should return a dict with all fields."""
        response = UserResponse(id="abc123", name="Alice", email="alice@example.com")

        data = response.model_dump()

        assert data == {"id": "abc123", "name": "Alice", "email": "alice@example.com"}

    def test_missing_required_field_raises_validation_error(self):
        """Constructing UserResponse without required fields should raise ValidationError."""
        with pytest.raises(ValidationError):
            UserResponse(id="abc123")  # type: ignore[call-arg]

    def test_wrong_type_raises_validation_error(self):
        """Constructing UserResponse with wrong field types should raise ValidationError."""
        with pytest.raises(ValidationError):
            UserResponse(id=123, name="Alice", email="alice@example.com")  # type: ignore[arg-type]
