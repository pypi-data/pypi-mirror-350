"""Tests for authentication commands."""

from unittest.mock import Mock, patch

import pytest
from click.testing import CliRunner

from ruru.commands.auth import auth_group
from ruru.exceptions import AuthenticationError, RuruAPIError


class TestAuthCommands:
    """Test authentication commands."""

    def test_auth_group_help(self, cli_runner: CliRunner):
        """Test that auth group shows help."""
        result = cli_runner.invoke(auth_group, ["--help"])
        assert result.exit_code == 0
        assert "Authentication commands" in result.output

    def test_init_command_help(self, cli_runner: CliRunner):
        """Test that init command shows help."""
        result = cli_runner.invoke(auth_group, ["init", "--help"])
        assert result.exit_code == 0
        assert "Initialize CLI with API credentials" in result.output

    @patch("ruru.commands.auth.ConfigManager")
    @patch("ruru.commands.auth.RuruClient")
    def test_init_command_success(
        self, mock_client_class, mock_config_class, cli_runner: CliRunner
    ):
        """Test successful init command."""
        # Setup mocks
        mock_config = Mock()
        mock_config_class.return_value = mock_config

        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.get_prompts.return_value = []  # Test API connection

        # Run command
        result = cli_runner.invoke(auth_group, ["init"], input="test-api-key\n")

        assert result.exit_code == 0
        assert "API key saved successfully" in result.output

        # Verify API key was set
        mock_config.set_api_key.assert_called_once_with("test-api-key")

        # Verify API connection was tested
        mock_client.get_prompts.assert_called_once()

    @patch("ruru.commands.auth.ConfigManager")
    @patch("ruru.commands.auth.RuruClient")
    def test_init_command_invalid_api_key(
        self, mock_client_class, mock_config_class, cli_runner: CliRunner
    ):
        """Test init command with invalid API key."""
        # Setup mocks
        mock_config = Mock()
        mock_config_class.return_value = mock_config

        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.get_prompts.side_effect = AuthenticationError("Invalid API key")

        # Run command
        result = cli_runner.invoke(auth_group, ["init"], input="invalid-key\n")

        assert result.exit_code == 1
        assert "Invalid API key" in result.output

        # Verify API key was not saved
        mock_config.set_api_key.assert_not_called()

    @patch("ruru.commands.auth.ConfigManager")
    @patch("ruru.commands.auth.RuruClient")
    def test_init_command_api_error(
        self, mock_client_class, mock_config_class, cli_runner: CliRunner
    ):
        """Test init command with API connection error."""
        # Setup mocks
        mock_config = Mock()
        mock_config_class.return_value = mock_config

        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.get_prompts.side_effect = RuruAPIError("Connection failed")

        # Run command
        result = cli_runner.invoke(auth_group, ["init"], input="test-key\n")

        assert result.exit_code == 1
        assert "Connection failed" in result.output

    def test_login_command_help(self, cli_runner: CliRunner):
        """Test that login command shows help."""
        result = cli_runner.invoke(auth_group, ["login", "--help"])
        assert result.exit_code == 0
        assert "Login with username and password" in result.output

    @patch("ruru.commands.auth.ConfigManager")
    @patch("ruru.commands.auth.RuruClient")
    def test_login_command_success(
        self, mock_client_class, mock_config_class, cli_runner: CliRunner
    ):
        """Test successful login command."""
        # Setup mocks
        mock_config = Mock()
        mock_config_class.return_value = mock_config

        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.login.return_value = {"api_key": "new-api-key"}

        # Run command
        result = cli_runner.invoke(auth_group, ["login"], input="testuser\ntestpass\n")

        assert result.exit_code == 0
        assert "Login successful" in result.output

        # Verify login was called
        mock_client.login.assert_called_once_with("testuser", "testpass")

        # Verify API key was saved
        mock_config.set_api_key.assert_called_once_with("new-api-key")

    @patch("ruru.commands.auth.ConfigManager")
    @patch("ruru.commands.auth.RuruClient")
    def test_login_command_invalid_credentials(
        self, mock_client_class, mock_config_class, cli_runner: CliRunner
    ):
        """Test login command with invalid credentials."""
        # Setup mocks
        mock_config = Mock()
        mock_config_class.return_value = mock_config

        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.login.side_effect = AuthenticationError("Invalid credentials")

        # Run command
        result = cli_runner.invoke(auth_group, ["login"], input="baduser\nbadpass\n")

        assert result.exit_code == 1
        assert "Invalid credentials" in result.output

        # Verify API key was not saved
        mock_config.set_api_key.assert_not_called()

    def test_logout_command_help(self, cli_runner: CliRunner):
        """Test that logout command shows help."""
        result = cli_runner.invoke(auth_group, ["logout", "--help"])
        assert result.exit_code == 0
        assert "Clear stored credentials" in result.output

    @patch("ruru.commands.auth.ConfigManager")
    def test_logout_command_success(self, mock_config_class, cli_runner: CliRunner):
        """Test successful logout command."""
        # Setup mocks
        mock_config = Mock()
        mock_config_class.return_value = mock_config

        # Run command
        result = cli_runner.invoke(auth_group, ["logout"])

        assert result.exit_code == 0
        assert "Logged out successfully" in result.output

        # Verify API key was cleared
        mock_config.clear_api_key.assert_called_once()

    def test_status_command_help(self, cli_runner: CliRunner):
        """Test that status command shows help."""
        result = cli_runner.invoke(auth_group, ["status", "--help"])
        assert result.exit_code == 0
        assert "Show authentication status" in result.output

    @patch("ruru.commands.auth.ConfigManager")
    def test_status_command_authenticated(
        self, mock_config_class, cli_runner: CliRunner
    ):
        """Test status command when authenticated."""
        # Setup mocks
        mock_config = Mock()
        mock_config_class.return_value = mock_config
        mock_config.get_api_key.return_value = "test-api-key"

        # Run command
        result = cli_runner.invoke(auth_group, ["status"])

        assert result.exit_code == 0
        assert "Authenticated" in result.output
        assert "API key is configured" in result.output

    @patch("ruru.commands.auth.ConfigManager")
    def test_status_command_not_authenticated(
        self, mock_config_class, cli_runner: CliRunner
    ):
        """Test status command when not authenticated."""
        # Setup mocks
        mock_config = Mock()
        mock_config_class.return_value = mock_config
        mock_config.get_api_key.return_value = None

        # Run command
        result = cli_runner.invoke(auth_group, ["status"])

        assert result.exit_code == 0
        assert "Not authenticated" in result.output
        assert "No API key found" in result.output

    def test_set_api_key_command_help(self, cli_runner: CliRunner):
        """Test that set-api-key command shows help."""
        result = cli_runner.invoke(auth_group, ["set-api-key", "--help"])
        assert result.exit_code == 0
        assert "Set API key manually" in result.output

    @patch("ruru.commands.auth.ConfigManager")
    @patch("ruru.commands.auth.RuruClient")
    def test_set_api_key_command_success(
        self, mock_client_class, mock_config_class, cli_runner: CliRunner
    ):
        """Test successful set-api-key command."""
        # Setup mocks
        mock_config = Mock()
        mock_config_class.return_value = mock_config

        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.get_prompts.return_value = []  # Test API connection

        # Run command
        result = cli_runner.invoke(auth_group, ["set-api-key", "new-api-key"])

        assert result.exit_code == 0
        assert "API key set successfully" in result.output

        # Verify API key was set
        mock_config.set_api_key.assert_called_once_with("new-api-key")

        # Verify API connection was tested
        mock_client.get_prompts.assert_called_once()

    @patch("ruru.commands.auth.ConfigManager")
    @patch("ruru.commands.auth.RuruClient")
    def test_set_api_key_command_invalid_key(
        self, mock_client_class, mock_config_class, cli_runner: CliRunner
    ):
        """Test set-api-key command with invalid key."""
        # Setup mocks
        mock_config = Mock()
        mock_config_class.return_value = mock_config

        mock_client = Mock()
        mock_client_class.return_value = mock_client
        mock_client.get_prompts.side_effect = AuthenticationError("Invalid API key")

        # Run command
        result = cli_runner.invoke(auth_group, ["set-api-key", "invalid-key"])

        assert result.exit_code == 1
        assert "Invalid API key" in result.output

        # Verify API key was not saved
        mock_config.set_api_key.assert_not_called()
