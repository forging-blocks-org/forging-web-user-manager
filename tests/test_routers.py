"""Tests for FastAPI user CRUD routes."""

import pytest
from fastapi.testclient import TestClient

from forging_web_user_manager.main import create_app


@pytest.fixture
def client() -> TestClient:
    """Return a TestClient wired to a fresh create_app instance."""
    app = create_app()
    return TestClient(app)


class TestCreateUser:
    """Tests for POST /users."""

    def test_creates_user_and_returns_201(self, client: TestClient):
        """POST /users with valid data should return 201 with UserResponse."""
        response = client.post(
            "/users",
            json={"name": "Alice", "email": "alice@example.com"},
        )

        assert response.status_code == 201
        body = response.json()
        assert body["name"] == "Alice"
        assert body["email"] == "alice@example.com"
        assert "id" in body
        assert len(body["id"]) > 0

    def test_invalid_email_returns_400(self, client: TestClient):
        """POST /users with an invalid email should return 400."""
        response = client.post(
            "/users",
            json={"name": "Alice", "email": "not-an-email"},
        )

        assert response.status_code == 400

    def test_empty_name_returns_400(self, client: TestClient):
        """POST /users with an empty name should return 400."""
        response = client.post(
            "/users",
            json={"name": "", "email": "alice@example.com"},
        )

        assert response.status_code == 400


class TestGetUser:
    """Tests for GET /users/{user_id}."""

    def test_returns_200_for_existing_user(self, client: TestClient):
        """GET /users/{user_id} should return 200 with UserResponse for an existing user."""
        create_resp = client.post(
            "/users",
            json={"name": "Alice", "email": "alice@example.com"},
        )
        user_id = create_resp.json()["id"]

        response = client.get(f"/users/{user_id}")

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == user_id
        assert body["name"] == "Alice"
        assert body["email"] == "alice@example.com"

    def test_returns_404_for_nonexistent_user(self, client: TestClient):
        """GET /users/{user_id} should return 404 for a non-existent user."""
        response = client.get("/users/nonexistent-id")

        assert response.status_code == 404


class TestListUsers:
    """Tests for GET /users."""

    def test_returns_200_with_empty_list_when_no_users(self, client: TestClient):
        """GET /users should return 200 with an empty list when no users exist."""
        response = client.get("/users")

        assert response.status_code == 200
        assert response.json() == []

    def test_returns_200_with_list_of_users(self, client: TestClient):
        """GET /users should return 200 with a list of all users."""
        client.post("/users", json={"name": "Alice", "email": "alice@example.com"})
        client.post("/users", json={"name": "Bob", "email": "bob@example.com"})

        response = client.get("/users")

        assert response.status_code == 200
        body = response.json()
        assert len(body) == 2
        names = {u["name"] for u in body}
        assert names == {"Alice", "Bob"}


class TestUpdateUser:
    """Tests for PUT /users/{user_id}."""

    def test_updates_user_and_returns_200(self, client: TestClient):
        """PUT /users/{user_id} with valid data should return 200 with updated UserResponse."""
        create_resp = client.post(
            "/users",
            json={"name": "Alice", "email": "alice@example.com"},
        )
        user_id = create_resp.json()["id"]

        response = client.put(
            f"/users/{user_id}",
            json={"name": "Alice Updated"},
        )

        assert response.status_code == 200
        body = response.json()
        assert body["id"] == user_id
        assert body["name"] == "Alice Updated"
        assert body["email"] == "alice@example.com"

    def test_returns_404_for_nonexistent_user(self, client: TestClient):
        """PUT /users/{user_id} with a non-existent id should return 404."""
        response = client.put(
            "/users/nonexistent-id",
            json={"name": "Ghost"},
        )

        assert response.status_code == 404


class TestDeleteUser:
    """Tests for DELETE /users/{user_id}."""

    def test_returns_204_for_existing_user(self, client: TestClient):
        """DELETE /users/{user_id} should return 204 for an existing user."""
        create_resp = client.post(
            "/users",
            json={"name": "Alice", "email": "alice@example.com"},
        )
        user_id = create_resp.json()["id"]

        response = client.delete(f"/users/{user_id}")

        assert response.status_code == 204

    def test_returns_404_for_nonexistent_user(self, client: TestClient):
        """DELETE /users/{user_id} should return 404 for a non-existent user."""
        response = client.delete("/users/nonexistent-id")

        assert response.status_code == 404
