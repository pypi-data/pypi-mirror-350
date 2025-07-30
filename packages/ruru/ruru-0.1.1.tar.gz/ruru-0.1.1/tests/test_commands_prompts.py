"""Tests for prompt management commands."""

from unittest.mock import Mock, patch, mock_open

import pytest
from click.testing import CliRunner

from ruru.commands.prompts import prompts_group
from ruru.exceptions import AuthenticationError, NotFoundError, RuruAPIError


class TestPromptCommands:
    """Test prompt management commands."""

    def test_prompts_group_help(self, cli_runner: CliRunner):
        """Test that prompts group shows help."""
        result = cli_runner.invoke(prompts_group, ["--help"])
        assert result.exit_code == 0
        assert "Prompt management commands" in result.output

    def test_list_command_help(self, cli_runner: CliRunner):
        """Test that list command shows help."""
        result = cli_runner.invoke(prompts_group, ["list", "--help"])
        assert result.exit_code == 0
        assert "List all prompts" in result.output

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_list_command_success(self, mock_get_client, cli_runner: CliRunner):
        """Test successful list command."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompts.return_value = [
            {
                "id": "123",
                "name": "test-prompt",
                "description": "Test prompt",
                "location": ".cursorrules",
                "tags": ["test", "cursor"],
                "created_at": "2024-01-01T00:00:00Z",
                "current_version": {"version_number": 1},
            }
        ]

        # Run command
        result = cli_runner.invoke(prompts_group, ["list"])

        assert result.exit_code == 0
        assert "test-prompt" in result.output
        assert ".cursorrules" in result.output

        # Verify client was called
        mock_client.get_prompts.assert_called_once()

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_list_command_with_filters(self, mock_get_client, cli_runner: CliRunner):
        """Test list command with filters."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompts.return_value = []

        # Run command with filters
        result = cli_runner.invoke(
            prompts_group, ["list", "--tags", "python,ai", "--location", ".cursorrules"]
        )

        assert result.exit_code == 0

        # Verify filters were passed
        mock_client.get_prompts.assert_called_once_with(
            tags=["python", "ai"], location=".cursorrules"
        )

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_list_command_authentication_error(
        self, mock_get_client, cli_runner: CliRunner
    ):
        """Test list command with authentication error."""
        mock_get_client.side_effect = AuthenticationError("Invalid API key")

        result = cli_runner.invoke(prompts_group, ["list"])

        assert result.exit_code == 1
        assert "Invalid API key" in result.output

    def test_get_command_help(self, cli_runner: CliRunner):
        """Test that get command shows help."""
        result = cli_runner.invoke(prompts_group, ["get", "--help"])
        assert result.exit_code == 0
        assert "Download a prompt" in result.output

    @patch("ruru.commands.prompts.get_authenticated_client")
    @patch("builtins.open", new_callable=mock_open)
    @patch("ruru.commands.prompts.Path")
    def test_get_command_success(
        self, mock_path, mock_file, mock_get_client, cli_runner: CliRunner
    ):
        """Test successful get command."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompt_by_name.return_value = {
            "id": "123",
            "name": "test-prompt",
            "location": ".cursorrules",
            "current_version": {"content": "Test prompt content"},
        }

        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.parent.exists.return_value = True

        # Run command
        result = cli_runner.invoke(prompts_group, ["get", "test-prompt"])

        assert result.exit_code == 0
        assert "Downloaded" in result.output

        # Verify file was written
        mock_file.assert_called_once()
        mock_file().write.assert_called_once_with("Test prompt content")

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_get_command_not_found(self, mock_get_client, cli_runner: CliRunner):
        """Test get command with prompt not found."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompt_by_name.side_effect = NotFoundError("Prompt not found")

        result = cli_runner.invoke(prompts_group, ["get", "nonexistent"])

        assert result.exit_code == 1
        assert "Prompt not found" in result.output

    def test_save_command_help(self, cli_runner: CliRunner):
        """Test that save command shows help."""
        result = cli_runner.invoke(prompts_group, ["save", "--help"])
        assert result.exit_code == 0
        assert "Upload a file as a prompt" in result.output

    @patch("ruru.commands.prompts.get_authenticated_client")
    @patch("builtins.open", new_callable=mock_open, read_data="Test content")
    @patch("ruru.commands.prompts.Path")
    def test_save_command_success(
        self, mock_path, mock_file, mock_get_client, cli_runner: CliRunner
    ):
        """Test successful save command."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.create_prompt.return_value = {
            "id": "123",
            "name": "test-prompt",
            "location": ".cursorrules",
        }

        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = True
        mock_path_instance.name = ".cursorrules"

        # Run command
        result = cli_runner.invoke(
            prompts_group,
            ["save", ".cursorrules", "--name", "test-prompt", "--tags", "test,cursor"],
        )

        assert result.exit_code == 0
        assert "Saved" in result.output

        # Verify prompt was created
        mock_client.create_prompt.assert_called_once()
        call_args = mock_client.create_prompt.call_args[0][0]
        assert call_args["name"] == "test-prompt"
        assert call_args["tags"] == ["test", "cursor"]
        assert call_args["content"] == "Test content"

    @patch("ruru.commands.prompts.Path")
    def test_save_command_file_not_found(self, mock_path, cli_runner: CliRunner):
        """Test save command with file not found."""
        mock_path_instance = Mock()
        mock_path.return_value = mock_path_instance
        mock_path_instance.exists.return_value = False

        result = cli_runner.invoke(prompts_group, ["save", "nonexistent.txt"])

        assert result.exit_code == 1
        assert "File not found" in result.output

    def test_delete_command_help(self, cli_runner: CliRunner):
        """Test that delete command shows help."""
        result = cli_runner.invoke(prompts_group, ["delete", "--help"])
        assert result.exit_code == 0
        assert "Delete a prompt" in result.output

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_delete_command_success(self, mock_get_client, cli_runner: CliRunner):
        """Test successful delete command."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompt_by_name.return_value = {
            "id": "123",
            "name": "test-prompt",
        }

        # Run command with confirmation
        result = cli_runner.invoke(
            prompts_group, ["delete", "test-prompt"], input="y\n"
        )

        assert result.exit_code == 0
        assert "Deleted" in result.output

        # Verify prompt was deleted
        mock_client.delete_prompt.assert_called_once_with("123")

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_delete_command_cancelled(self, mock_get_client, cli_runner: CliRunner):
        """Test delete command cancelled by user."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompt_by_name.return_value = {
            "id": "123",
            "name": "test-prompt",
        }

        # Run command and cancel
        result = cli_runner.invoke(
            prompts_group, ["delete", "test-prompt"], input="n\n"
        )

        assert result.exit_code == 0
        assert "Cancelled" in result.output

        # Verify prompt was not deleted
        mock_client.delete_prompt.assert_not_called()

    def test_info_command_help(self, cli_runner: CliRunner):
        """Test that info command shows help."""
        result = cli_runner.invoke(prompts_group, ["info", "--help"])
        assert result.exit_code == 0
        assert "Show prompt details" in result.output

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_info_command_success(self, mock_get_client, cli_runner: CliRunner):
        """Test successful info command."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompt_by_name.return_value = {
            "id": "123",
            "name": "test-prompt",
            "description": "Test description",
            "location": ".cursorrules",
            "tags": ["test", "cursor"],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T01:00:00Z",
            "current_version": {
                "version_number": 2,
                "created_at": "2024-01-01T01:00:00Z",
            },
        }

        # Run command
        result = cli_runner.invoke(prompts_group, ["info", "test-prompt"])

        assert result.exit_code == 0
        assert "test-prompt" in result.output
        assert "Test description" in result.output
        assert ".cursorrules" in result.output
        assert "test, cursor" in result.output

    def test_search_command_help(self, cli_runner: CliRunner):
        """Test that search command shows help."""
        result = cli_runner.invoke(prompts_group, ["search", "--help"])
        assert result.exit_code == 0
        assert "Search prompts by content" in result.output

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_search_command_success(self, mock_get_client, cli_runner: CliRunner):
        """Test successful search command."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.search_prompts.return_value = [
            {
                "id": "123",
                "name": "cursor-rules",
                "description": "Cursor rules for Python",
                "location": ".cursorrules",
                "tags": ["cursor", "python"],
            }
        ]

        # Run command
        result = cli_runner.invoke(prompts_group, ["search", "cursor rules"])

        assert result.exit_code == 0
        assert "cursor-rules" in result.output

        # Verify search was called
        mock_client.search_prompts.assert_called_once_with("cursor rules")

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_search_command_no_results(self, mock_get_client, cli_runner: CliRunner):
        """Test search command with no results."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.search_prompts.return_value = []

        # Run command
        result = cli_runner.invoke(prompts_group, ["search", "nonexistent"])

        assert result.exit_code == 0
        assert "No prompts found" in result.output

        # Verify search was called
        mock_client.search_prompts.assert_called_once_with("nonexistent")

    def test_show_command_help(self, cli_runner: CliRunner):
        """Test that show command shows help."""
        result = cli_runner.invoke(prompts_group, ["show", "--help"])
        assert result.exit_code == 0
        assert "Display prompt content" in result.output

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_show_command_success(self, mock_get_client, cli_runner: CliRunner):
        """Test successful show command."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompt_by_name.return_value = {
            "id": "123",
            "name": "test-prompt",
            "description": "Test prompt description",
            "location": ".cursorrules",
            "tags": ["test", "cursor"],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "current_version": {
                "version_number": 1,
                "content": "Test prompt content\nwith multiple lines",
            },
        }

        # Run command
        result = cli_runner.invoke(prompts_group, ["show", "test-prompt"])

        assert result.exit_code == 0
        assert "test-prompt" in result.output
        assert "Test prompt content" in result.output

        # Verify client was called
        mock_client.get_prompt_by_name.assert_called_once_with("test-prompt")

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_show_command_with_version(self, mock_get_client, cli_runner: CliRunner):
        """Test show command with specific version."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompt_by_name.return_value = {
            "id": "123",
            "name": "test-prompt",
            "description": "Test prompt description",
            "location": ".cursorrules",
            "tags": ["test", "cursor"],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "current_version": {
                "version_number": 2,
                "content": "Current version content",
            },
        }
        mock_client.get_versions.return_value = [
            {
                "id": "v1",
                "version_number": 1,
                "content": "Version 1 content",
                "created_at": "2024-01-01T00:00:00Z",
            },
            {
                "id": "v2",
                "version_number": 2,
                "content": "Version 2 content",
                "created_at": "2024-01-02T00:00:00Z",
            },
        ]

        # Run command with specific version
        result = cli_runner.invoke(
            prompts_group, ["show", "test-prompt", "--version", "1"]
        )

        assert result.exit_code == 0
        assert "Version 1 content" in result.output

        # Verify client was called
        mock_client.get_prompt_by_name.assert_called_once_with("test-prompt")
        mock_client.get_versions.assert_called_once_with("123")

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_show_command_version_not_found(
        self, mock_get_client, cli_runner: CliRunner
    ):
        """Test show command with non-existent version."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompt_by_name.return_value = {
            "id": "123",
            "name": "test-prompt",
            "description": "Test description",
            "location": ".cursorrules",
            "tags": ["test"],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "current_version": {"version_number": 1},
        }
        mock_client.get_versions.return_value = [
            {"id": "v1", "version_number": 1, "content": "Version 1 content"}
        ]

        # Run command with non-existent version
        result = cli_runner.invoke(
            prompts_group, ["show", "test-prompt", "--version", "99"]
        )

        assert result.exit_code == 1
        assert "Version 99 not found" in result.output

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_show_command_no_syntax(self, mock_get_client, cli_runner: CliRunner):
        """Test show command with syntax highlighting disabled."""
        # Setup mocks
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompt_by_name.return_value = {
            "id": "123",
            "name": "test-prompt",
            "description": "Test description",
            "location": ".cursorrules",
            "tags": ["test"],
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "current_version": {
                "version_number": 1,
                "content": "Test content without syntax highlighting",
            },
        }

        # Run command with --no-syntax flag
        result = cli_runner.invoke(
            prompts_group, ["show", "test-prompt", "--no-syntax"]
        )

        assert result.exit_code == 0
        assert "Test content without syntax highlighting" in result.output

    @patch("ruru.commands.prompts.get_authenticated_client")
    def test_show_command_not_found(self, mock_get_client, cli_runner: CliRunner):
        """Test show command with prompt not found."""
        mock_client = Mock()
        mock_get_client.return_value = mock_client
        mock_client.get_prompt_by_name.side_effect = NotFoundError("Prompt not found")

        result = cli_runner.invoke(prompts_group, ["show", "nonexistent"])

        assert result.exit_code == 1
        assert "Prompt not found" in result.output
