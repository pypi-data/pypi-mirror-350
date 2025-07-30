"""Tests for the HTTP API client."""

import json
from unittest.mock import Mock, patch

import httpx
import pytest
from pytest_httpx import HTTPXMock

from ruru.client import RuruClient
from ruru.config import Config
from ruru.exceptions import (
    AuthenticationError,
    NotFoundError,
    RuruAPIError,
    ValidationError,
)


class TestRuruClient:
    """Test the RuruClient HTTP client."""

    def test_client_init_with_config(self, isolated_env):
        """Test client initialization with config."""
        config = Config(api_url="https://test.api.com", api_timeout=60)
        client = RuruClient(config=config, api_key="test-key")

        assert client.base_url == "https://test.api.com"
        assert client.api_key == "test-key"
        assert client.timeout == 60

    def test_client_init_with_defaults(self, isolated_env):
        """Test client initialization with default config."""
        client = RuruClient(api_key="test-key")

        assert client.base_url == "https://api.ruru.dev"
        assert client.api_key == "test-key"
        assert client.timeout == 30

    def test_client_headers(self, isolated_env):
        """Test that client sets correct headers."""
        client = RuruClient(api_key="test-key")
        headers = client._get_headers()

        assert headers["Authorization"] == "Bearer test-key"
        assert headers["Content-Type"] == "application/json"
        assert "User-Agent" in headers
        assert "ruru-cli" in headers["User-Agent"]

    def test_get_prompts_success(self, isolated_env, httpx_mock: HTTPXMock):
        """Test successful prompts retrieval."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.ruru.dev/prompts",
            json={
                "prompts": [
                    {
                        "id": "123",
                        "name": "test-prompt",
                        "description": "A test prompt",
                        "location": ".cursorrules",
                        "tags": ["test"],
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "current_version": {
                            "id": "456",
                            "version_number": 1,
                            "content": "Test content",
                            "created_at": "2024-01-01T00:00:00Z",
                            "is_current": True,
                        },
                    }
                ]
            },
            status_code=200,
        )

        client = RuruClient(api_key="test-key")
        prompts = client.get_prompts()

        assert len(prompts) == 1
        assert prompts[0]["name"] == "test-prompt"
        assert prompts[0]["location"] == ".cursorrules"

    def test_get_prompts_with_filters(self, isolated_env):
        """Test prompts retrieval with filters."""
        responses.add(
            responses.GET,
            "https://api.ruru.dev/prompts",
            json={"prompts": []},
            status=200,
        )

        client = RuruClient(api_key="test-key")
        client.get_prompts(tags=["python", "ai"], location=".cursorrules")

        # Check that the request was made with correct query parameters
        request = responses.calls[0].request
        assert "tags=python%2Cai" in request.url
        assert "location=.cursorrules" in request.url

    def test_get_prompt_by_name_success(self, isolated_env):
        """Test successful prompt retrieval by name."""
        responses.add(
            responses.GET,
            "https://api.ruru.dev/prompts/by-name/test-prompt",
            json={
                "id": "123",
                "name": "test-prompt",
                "description": "A test prompt",
                "location": ".cursorrules",
                "tags": ["test"],
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "current_version": {
                    "id": "456",
                    "version_number": 1,
                    "content": "Test content",
                    "created_at": "2024-01-01T00:00:00Z",
                    "is_current": True,
                },
            },
            status=200,
        )

        client = RuruClient(api_key="test-key")
        prompt = client.get_prompt_by_name("test-prompt")

        assert prompt["name"] == "test-prompt"
        assert prompt["current_version"]["content"] == "Test content"

    def test_get_prompt_by_name_not_found(self, isolated_env):
        """Test prompt not found error."""
        responses.add(
            responses.GET,
            "https://api.ruru.dev/prompts/by-name/nonexistent",
            json={"detail": "Prompt not found"},
            status=404,
        )

        client = RuruClient(api_key="test-key")

        with pytest.raises(NotFoundError) as exc_info:
            client.get_prompt_by_name("nonexistent")

        assert "Prompt not found" in str(exc_info.value)

    def test_create_prompt_success(self, isolated_env):
        """Test successful prompt creation."""
        responses.add(
            responses.POST,
            "https://api.ruru.dev/prompts",
            json={
                "id": "123",
                "name": "new-prompt",
                "description": "A new prompt",
                "location": ".cursorrules",
                "tags": ["new"],
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T00:00:00Z",
                "current_version": {
                    "id": "456",
                    "version_number": 1,
                    "content": "New content",
                    "created_at": "2024-01-01T00:00:00Z",
                    "is_current": True,
                },
            },
            status=201,
        )

        client = RuruClient(api_key="test-key")
        prompt_data = {
            "name": "new-prompt",
            "description": "A new prompt",
            "location": ".cursorrules",
            "tags": ["new"],
            "content": "New content",
        }

        prompt = client.create_prompt(prompt_data)

        assert prompt["name"] == "new-prompt"
        assert prompt["current_version"]["content"] == "New content"

    def test_create_prompt_validation_error(self, isolated_env):
        """Test prompt creation validation error."""
        responses.add(
            responses.POST,
            "https://api.ruru.dev/prompts",
            json={
                "detail": [
                    {
                        "loc": ["name"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
            status=422,
        )

        client = RuruClient(api_key="test-key")

        with pytest.raises(ValidationError) as exc_info:
            client.create_prompt({"content": "test"})

        assert "field required" in str(exc_info.value)

    def test_update_prompt_success(self, isolated_env):
        """Test successful prompt update."""
        responses.add(
            responses.PUT,
            "https://api.ruru.dev/prompts/123",
            json={
                "id": "123",
                "name": "updated-prompt",
                "description": "Updated description",
                "location": ".cursorrules",
                "tags": ["updated"],
                "created_at": "2024-01-01T00:00:00Z",
                "updated_at": "2024-01-01T01:00:00Z",
                "current_version": {
                    "id": "456",
                    "version_number": 1,
                    "content": "Original content",
                    "created_at": "2024-01-01T00:00:00Z",
                    "is_current": True,
                },
            },
            status=200,
        )

        client = RuruClient(api_key="test-key")
        update_data = {
            "name": "updated-prompt",
            "description": "Updated description",
            "tags": ["updated"],
        }

        prompt = client.update_prompt("123", update_data)

        assert prompt["name"] == "updated-prompt"
        assert prompt["description"] == "Updated description"

    def test_delete_prompt_success(self, isolated_env):
        """Test successful prompt deletion."""
        responses.add(responses.DELETE, "https://api.ruru.dev/prompts/123", status=204)

        client = RuruClient(api_key="test-key")
        client.delete_prompt("123")

        # Should not raise any exception

    def test_create_version_success(self, isolated_env):
        """Test successful version creation."""
        responses.add(
            responses.POST,
            "https://api.ruru.dev/prompts/123/versions",
            json={
                "id": "789",
                "version_number": 2,
                "content": "Updated content",
                "commit_message": "Updated prompt",
                "created_at": "2024-01-01T01:00:00Z",
                "is_current": True,
            },
            status=201,
        )

        client = RuruClient(api_key="test-key")
        version_data = {
            "content": "Updated content",
            "commit_message": "Updated prompt",
        }

        version = client.create_version("123", version_data)

        assert version["version_number"] == 2
        assert version["content"] == "Updated content"
        assert version["commit_message"] == "Updated prompt"

    def test_get_versions_success(self, isolated_env):
        """Test successful versions retrieval."""
        responses.add(
            responses.GET,
            "https://api.ruru.dev/prompts/123/versions",
            json={
                "versions": [
                    {
                        "id": "456",
                        "version_number": 1,
                        "content": "Original content",
                        "created_at": "2024-01-01T00:00:00Z",
                        "is_current": False,
                    },
                    {
                        "id": "789",
                        "version_number": 2,
                        "content": "Updated content",
                        "created_at": "2024-01-01T01:00:00Z",
                        "is_current": True,
                    },
                ]
            },
            status=200,
        )

        client = RuruClient(api_key="test-key")
        versions = client.get_versions("123")

        assert len(versions) == 2
        assert versions[0]["version_number"] == 1
        assert versions[1]["version_number"] == 2
        assert versions[1]["is_current"] is True

    def test_authentication_error(self, isolated_env):
        """Test authentication error handling."""
        responses.add(
            responses.GET,
            "https://api.ruru.dev/prompts",
            json={"detail": "Invalid API key"},
            status=401,
        )

        client = RuruClient(api_key="invalid-key")

        with pytest.raises(AuthenticationError) as exc_info:
            client.get_prompts()

        assert "Invalid API key" in str(exc_info.value)

    def test_server_error(self, isolated_env):
        """Test server error handling."""
        responses.add(
            responses.GET,
            "https://api.ruru.dev/prompts",
            json={"detail": "Internal server error"},
            status=500,
        )

        client = RuruClient(api_key="test-key")

        with pytest.raises(RuruAPIError) as exc_info:
            client.get_prompts()

        assert "Internal server error" in str(exc_info.value)

    def test_network_error(self, isolated_env):
        """Test network error handling."""
        client = RuruClient(api_key="test-key")

        with patch.object(client, "_make_request") as mock_request:
            mock_request.side_effect = httpx.ConnectError("Connection failed")

            with pytest.raises(RuruAPIError) as exc_info:
                client.get_prompts()

            assert "Connection failed" in str(exc_info.value)

    def test_search_prompts_query_encoding(self, isolated_env):
        """Test that search queries are properly encoded."""
        client = RuruClient(api_key="test-key")

        with patch.object(client, "_make_request") as mock_request:
            mock_request.return_value = {"prompts": []}

            client.search_prompts("cursor rules & python")

            # Check that the query was properly encoded
            mock_request.assert_called_once()
            args, kwargs = mock_request.call_args
            assert "cursor%20rules%20%26%20python" in args[1]
