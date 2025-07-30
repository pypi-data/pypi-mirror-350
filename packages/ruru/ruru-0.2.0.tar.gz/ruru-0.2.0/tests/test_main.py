"""Tests for the main CLI entry point."""

import pytest
from click.testing import CliRunner

from ruru.main import cli


class TestMainCLI:
    """Test the main CLI entry point."""

    def test_cli_help(self, cli_runner: CliRunner):
        """Test that the CLI shows help when called with --help."""
        result = cli_runner.invoke(cli, ["--help"])
        assert result.exit_code == 0
        assert "ruru" in result.output.lower()
        assert "Usage:" in result.output

    def test_cli_version(self, cli_runner: CliRunner):
        """Test that the CLI shows version when called with --version."""
        result = cli_runner.invoke(cli, ["--version"])
        assert result.exit_code == 0
        assert "version" in result.output.lower()

    def test_cli_no_args(self, cli_runner: CliRunner):
        """Test that the CLI shows help when called without arguments."""
        result = cli_runner.invoke(cli, [])
        assert result.exit_code == 0
        assert "Usage:" in result.output

    def test_cli_invalid_command(self, cli_runner: CliRunner):
        """Test that the CLI shows error for invalid commands."""
        result = cli_runner.invoke(cli, ["invalid-command"])
        assert result.exit_code != 0
        assert "No such command" in result.output
