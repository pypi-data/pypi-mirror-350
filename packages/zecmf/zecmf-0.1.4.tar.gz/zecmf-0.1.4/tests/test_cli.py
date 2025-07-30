"""Tests for CLI commands."""

from unittest.mock import MagicMock, patch

from flask import Flask

from zecmf.cli.commands import (
    health_check_impl,
    register_commands,
)


def test_register_commands() -> None:
    """Test that commands are registered with the app."""
    app = Flask("test")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"

    # Reset mocks to ensure clean state
    with patch.object(app.cli, "add_command", MagicMock()) as mock_add_command:
        # Execute the function
        register_commands(app)

        # Get the commands that were registered
        called_with = [args[0] for args, _ in mock_add_command.call_args_list]

        # Verify each command was registered by its name
        command_names = [cmd.name for cmd in called_with]
        assert "setup-db" in command_names
        assert "health-check" in command_names
        assert "init-migrations" in command_names


def test_health_check_success() -> None:
    """Test health check command when all systems are operational."""
    app = Flask("test")
    db_mock = MagicMock()
    db_mock.session.execute.return_value = "Success"

    with (
        patch("zecmf.cli.commands.db", db_mock),
        patch("zecmf.cli.commands.current_app", app),
        patch("click.echo") as mock_echo,
    ):
        # Run the implementation function directly instead of the command
        health_check_impl()

        # Verify outputs
        mock_echo.assert_any_call("Checking application health...")
        mock_echo.assert_any_call("Database connection: OK")
        mock_echo.assert_any_call("All systems operational!")


def test_health_check_database_failure() -> None:
    """Test health check command when database connection fails."""
    app = Flask("test")
    db_mock = MagicMock()
    db_mock.session.execute.side_effect = Exception("Database connection error")

    with (
        patch("zecmf.cli.commands.db", db_mock),
        patch("zecmf.cli.commands.current_app", app),
        patch("click.echo") as mock_echo,
    ):
        # Run the implementation function directly
        health_check_impl()

        # Verify outputs
        mock_echo.assert_any_call("Checking application health...")
        mock_echo.assert_any_call(
            "Database connection: FAILED (Database connection error)"
        )
