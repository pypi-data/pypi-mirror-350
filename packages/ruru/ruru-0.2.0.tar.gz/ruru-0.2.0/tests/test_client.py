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

        assert headers["X-API-Key"] == "test-key"
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

    def test_get_prompts_with_filters(self, isolated_env, httpx_mock: HTTPXMock):
        """Test prompts retrieval with filters."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.ruru.dev/prompts?tags=python%2Cai&location=.cursorrules",
            json={"prompts": []},
            status_code=200,
        )

        client = RuruClient(api_key="test-key")
        client.get_prompts(tags=["python", "ai"], location=".cursorrules")

        # Verify the request was made
        assert len(httpx_mock.get_requests()) == 1

    def test_get_prompt_by_name_success(self, isolated_env, httpx_mock: HTTPXMock):
        """Test successful prompt retrieval by name."""
        # Mock the get_prompts call that get_prompt_by_name uses internally
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
        prompt = client.get_prompt_by_name("test-prompt")

        assert prompt["name"] == "test-prompt"
        assert prompt["current_version"]["content"] == "Test content"

    def test_get_prompt_by_name_not_found(self, isolated_env, httpx_mock: HTTPXMock):
        """Test prompt not found error."""
        # Mock empty prompts list to simulate prompt not found
        httpx_mock.add_response(
            method="GET",
            url="https://api.ruru.dev/prompts",
            json={"prompts": []},
            status_code=200,
        )

        client = RuruClient(api_key="test-key")

        with pytest.raises(NotFoundError) as exc_info:
            client.get_prompt_by_name("nonexistent")

        assert "Prompt 'nonexistent' not found" in str(exc_info.value)

    def test_create_prompt_success(self, isolated_env, httpx_mock: HTTPXMock):
        """Test successful prompt creation."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.ruru.dev/prompts",
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
            status_code=201,
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

    def test_create_prompt_validation_error(self, isolated_env, httpx_mock: HTTPXMock):
        """Test prompt creation validation error."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.ruru.dev/prompts",
            json={
                "detail": [
                    {
                        "loc": ["name"],
                        "msg": "field required",
                        "type": "value_error.missing",
                    }
                ]
            },
            status_code=422,
        )

        client = RuruClient(api_key="test-key")

        with pytest.raises(ValidationError) as exc_info:
            client.create_prompt({"content": "test"})

        assert "field required" in str(exc_info.value)

    def test_update_prompt_success(self, isolated_env, httpx_mock: HTTPXMock):
        """Test successful prompt update."""
        httpx_mock.add_response(
            method="PUT",
            url="https://api.ruru.dev/prompts/123",
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
            status_code=200,
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

    def test_delete_prompt_success(self, isolated_env, httpx_mock: HTTPXMock):
        """Test successful prompt deletion."""
        httpx_mock.add_response(
            method="DELETE", url="https://api.ruru.dev/prompts/123", status_code=204
        )

        client = RuruClient(api_key="test-key")
        client.delete_prompt("123")

        # Should not raise any exception

    def test_create_version_success(self, isolated_env, httpx_mock: HTTPXMock):
        """Test successful version creation."""
        httpx_mock.add_response(
            method="POST",
            url="https://api.ruru.dev/prompts/123/versions",
            json={
                "id": "789",
                "version_number": 2,
                "content": "Updated content",
                "commit_message": "Updated prompt",
                "created_at": "2024-01-01T01:00:00Z",
                "is_current": True,
            },
            status_code=201,
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

    def test_get_versions_success(self, isolated_env, httpx_mock: HTTPXMock):
        """Test successful versions retrieval."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.ruru.dev/prompts/123/versions",
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
            status_code=200,
        )

        client = RuruClient(api_key="test-key")
        versions = client.get_versions("123")

        assert len(versions) == 2
        assert versions[0]["version_number"] == 1
        assert versions[1]["version_number"] == 2
        assert versions[1]["is_current"] is True

    def test_authentication_error(self, isolated_env, httpx_mock: HTTPXMock):
        """Test authentication error handling."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.ruru.dev/prompts",
            json={"detail": "Invalid API key"},
            status_code=401,
        )

        client = RuruClient(api_key="invalid-key")

        with pytest.raises(AuthenticationError) as exc_info:
            client.get_prompts()

        assert "Invalid API key" in str(exc_info.value)

    def test_server_error(self, isolated_env, httpx_mock: HTTPXMock):
        """Test server error handling."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.ruru.dev/prompts",
            json={"detail": "Internal server error"},
            status_code=500,
        )

        client = RuruClient(api_key="test-key")

        with pytest.raises(RuruAPIError) as exc_info:
            client.get_prompts()

        assert "Internal server error" in str(exc_info.value)

    def test_network_error(self, isolated_env):
        """Test network error handling."""
        client = RuruClient(api_key="test-key")

        with patch.object(client, "_make_request") as mock_request:
            mock_request.side_effect = RuruAPIError("Request failed: Connection failed")

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
            # The endpoint should be /prompts/search and params should contain the encoded query
            assert args[1] == "/prompts/search"
            assert "q" in kwargs["params"]
            assert kwargs["params"]["q"] == "cursor rules & python"

    def test_download_prompts_success(self, isolated_env, httpx_mock: HTTPXMock):
        """Test successful prompts download."""
        # Use a pattern to match any URL with the base path
        import re

        httpx_mock.add_response(
            method="GET",
            url=re.compile(r"https://api\.ruru\.dev/prompts/download.*"),
            json={
                "prompts": [
                    {
                        "id": "123",
                        "name": "test-prompt",
                        "description": "Test description",
                        "location": ".cursorrules",
                        "tags": ["test"],
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "current_version": {
                            "version_number": 1,
                            "content": "Test content",
                        },
                    }
                ],
                "total": 1,
                "filters_applied": {"project_name": "test-project"},
            },
            status_code=200,
        )

        client = RuruClient(api_key="test-key")
        response = client.download_prompts(
            project_name="test-project",
            tags=["python", "ai"],
            include_content=True,
            format="json",
        )

        assert response["total"] == 1
        assert len(response["prompts"]) == 1
        assert response["prompts"][0]["name"] == "test-prompt"
        assert response["filters_applied"]["project_name"] == "test-project"

    def test_download_prompts_zip_success(self, isolated_env, httpx_mock: HTTPXMock):
        """Test successful prompts ZIP download."""
        import re

        zip_content = b"fake zip content"
        httpx_mock.add_response(
            method="GET",
            url=re.compile(r"https://api\.ruru\.dev/prompts/download/zip.*"),
            content=zip_content,
            status_code=200,
            headers={"content-type": "application/zip"},
        )

        client = RuruClient(api_key="test-key")
        result = client.download_prompts_zip(
            project_name="test-project", tags=["python", "ai"]
        )

        assert result == zip_content

    def test_download_prompts_by_project_success(
        self, isolated_env, httpx_mock: HTTPXMock
    ):
        """Test successful project prompts download."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.ruru.dev/prompts/download/by-project/test-project?include_content=true",
            json={
                "prompts": [
                    {
                        "id": "123",
                        "name": "project-prompt",
                        "description": "Project prompt",
                        "location": ".cursorrules",
                        "tags": ["project"],
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "current_version": {
                            "version_number": 1,
                            "content": "Project content",
                        },
                    }
                ],
                "total": 1,
            },
            status_code=200,
        )

        client = RuruClient(api_key="test-key")
        response = client.download_prompts_by_project(
            project_name="test-project", include_content=True
        )

        assert response["total"] == 1
        assert len(response["prompts"]) == 1
        assert response["prompts"][0]["name"] == "project-prompt"

    def test_download_prompts_by_directory_success(
        self, isolated_env, httpx_mock: HTTPXMock
    ):
        """Test successful directory prompts download."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.ruru.dev/prompts/download/by-directory?directory=src%2F%2A&include_content=true",
            json={
                "prompts": [
                    {
                        "id": "123",
                        "name": "dir-prompt",
                        "description": "Directory prompt",
                        "location": "src/.cursorrules",
                        "tags": ["directory"],
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "current_version": {
                            "version_number": 1,
                            "content": "Directory content",
                        },
                    }
                ],
                "total": 1,
            },
            status_code=200,
        )

        client = RuruClient(api_key="test-key")
        response = client.download_prompts_by_directory(
            directory="src/*", include_content=True
        )

        assert response["total"] == 1
        assert len(response["prompts"]) == 1
        assert response["prompts"][0]["name"] == "dir-prompt"

    def test_download_prompts_by_tags_success(
        self, isolated_env, httpx_mock: HTTPXMock
    ):
        """Test successful tags prompts download."""
        import re

        httpx_mock.add_response(
            method="GET",
            url=re.compile(r"https://api\.ruru\.dev/prompts/download/by-tags.*"),
            json={
                "prompts": [
                    {
                        "id": "123",
                        "name": "tagged-prompt",
                        "description": "Tagged prompt",
                        "location": ".cursorrules",
                        "tags": ["python", "ai"],
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "current_version": {
                            "version_number": 1,
                            "content": "Tagged content",
                        },
                    }
                ],
                "total": 1,
            },
            status_code=200,
        )

        client = RuruClient(api_key="test-key")
        response = client.download_prompts_by_tags(
            tags=["python", "ai"], include_content=True
        )

        assert response["total"] == 1
        assert len(response["prompts"]) == 1
        assert response["prompts"][0]["name"] == "tagged-prompt"
        assert "python" in response["prompts"][0]["tags"]
        assert "ai" in response["prompts"][0]["tags"]

    def test_download_prompts_authentication_error(
        self, isolated_env, httpx_mock: HTTPXMock
    ):
        """Test download prompts authentication error."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.ruru.dev/prompts/download?include_content=true&format=json",
            json={"detail": "Invalid API key"},
            status_code=401,
        )

        client = RuruClient(api_key="invalid-key")

        with pytest.raises(AuthenticationError) as exc_info:
            client.download_prompts()

        assert "Invalid API key" in str(exc_info.value)

    def test_download_prompts_zip_not_found(self, isolated_env, httpx_mock: HTTPXMock):
        """Test download prompts ZIP not found error."""
        httpx_mock.add_response(
            method="GET",
            url="https://api.ruru.dev/prompts/download/zip",
            json={"detail": "No prompts found"},
            status_code=404,
        )

        client = RuruClient(api_key="test-key")

        with pytest.raises(NotFoundError) as exc_info:
            client.download_prompts_zip()

        assert "No prompts found" in str(exc_info.value)
