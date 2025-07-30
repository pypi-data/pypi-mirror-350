"""Additional unit tests for fabric_mcp.cli module."""

import sys
from unittest.mock import Mock, patch

import pytest

from fabric_mcp import __version__
from fabric_mcp.cli import main


class TestCLIMain:
    """Test cases for the main CLI function."""

    def test_version_flag(self, capsys: pytest.CaptureFixture[str]):
        """Test --version flag displays version and exits."""
        with patch.object(sys, "argv", ["fabric-mcp", "--version"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            # argparse --version action exits with code 0
            assert exc_info.value.code == 0

            # Check that version was printed to stdout
            captured = capsys.readouterr()
            assert f"fabric-mcp {__version__}" in captured.out

    def test_help_flag(self, capsys: pytest.CaptureFixture[str]):
        """Test --help flag displays help and exits."""
        with patch.object(sys, "argv", ["fabric-mcp", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            # argparse --help action exits with code 0
            assert exc_info.value.code == 0

            # Check that help was printed
            captured = capsys.readouterr()
            assert "A Model Context Protocol server for Fabric AI" in captured.out
            assert "--stdio" in captured.out
            assert "--log-level" in captured.out

    def test_no_args_shows_help_and_exits(self, capsys: pytest.CaptureFixture[str]):
        """Test that running with no arguments shows help and exits with error."""
        with patch.object(sys, "argv", ["fabric-mcp"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            # Should exit with error code
            assert exc_info.value.code == 1

            # Check that help was printed to stderr
            captured = capsys.readouterr()
            assert "A Model Context Protocol server for Fabric AI" in captured.err

    def test_only_log_level_without_stdio_shows_help(
        self, capsys: pytest.CaptureFixture[str]
    ):
        """Test that only --log-level without --stdio shows help."""
        with patch.object(sys, "argv", ["fabric-mcp", "--log-level", "debug"]):
            with pytest.raises(SystemExit) as exc_info:
                main()

            assert exc_info.value.code == 1
            captured = capsys.readouterr()
            assert "A Model Context Protocol server for Fabric AI" in captured.err

    @patch("fabric_mcp.cli.FabricMCP")
    @patch("fabric_mcp.cli.Log")
    def test_stdio_flag_creates_server_and_runs(
        self, mock_log_class: Mock, mock_fabric_mcp_class: Mock
    ):
        """Test that --stdio flag creates server and runs it."""
        # Setup mocks
        mock_log = Mock()
        mock_log.level_name = "INFO"
        mock_log.logger = Mock()
        mock_log_class.return_value = mock_log

        mock_server = Mock()
        mock_fabric_mcp_class.return_value = mock_server

        with patch.object(sys, "argv", ["fabric-mcp", "--stdio"]):
            main()

        # Verify Log was created with correct level
        mock_log_class.assert_called_once_with("info")

        # Verify FabricMCP was created with correct log level
        mock_fabric_mcp_class.assert_called_once_with(log_level="INFO")

        # Verify stdio() was called
        mock_server.stdio.assert_called_once()

    @patch("fabric_mcp.cli.FabricMCP")
    @patch("fabric_mcp.cli.Log")
    def test_stdio_with_custom_log_level(
        self, mock_log_class: Mock, mock_fabric_mcp_class: Mock
    ):
        """Test --stdio with custom log level."""
        mock_log = Mock()
        mock_log.level_name = "DEBUG"
        mock_log.logger = Mock()
        mock_log_class.return_value = mock_log

        mock_server = Mock()
        mock_fabric_mcp_class.return_value = mock_server

        with patch.object(
            sys, "argv", ["fabric-mcp", "--stdio", "--log-level", "debug"]
        ):
            main()

        # Verify Log was created with debug level
        mock_log_class.assert_called_once_with("debug")

        # Verify FabricMCP was created with DEBUG log level
        mock_fabric_mcp_class.assert_called_once_with(log_level="DEBUG")

    @patch("fabric_mcp.cli.FabricMCP")
    @patch("fabric_mcp.cli.Log")
    def test_stdio_with_short_log_level_flag(
        self, mock_log_class: Mock, mock_fabric_mcp_class: Mock
    ):
        """Test --stdio with short form -l for log level."""
        mock_log = Mock()
        mock_log.level_name = "ERROR"
        mock_log.logger = Mock()
        mock_log_class.return_value = mock_log

        mock_server = Mock()
        mock_fabric_mcp_class.return_value = mock_server

        with patch.object(sys, "argv", ["fabric-mcp", "--stdio", "-l", "error"]):
            main()

        mock_log_class.assert_called_once_with("error")
        mock_fabric_mcp_class.assert_called_once_with(log_level="ERROR")

    @patch("fabric_mcp.cli.FabricMCP")
    @patch("fabric_mcp.cli.Log")
    def test_stdio_logs_startup_and_shutdown_messages(
        self, mock_log_class: Mock, mock_fabric_mcp_class: Mock
    ):
        """Test that appropriate log messages are generated."""
        mock_log = Mock()
        mock_log.level_name = "INFO"
        mock_logger = Mock()
        mock_log.logger = mock_logger
        mock_log_class.return_value = mock_log

        mock_server = Mock()
        mock_fabric_mcp_class.return_value = mock_server

        with patch.object(sys, "argv", ["fabric-mcp", "--stdio"]):
            main()

        # Check that startup message was logged
        startup_calls = [
            call
            for call in mock_logger.info.call_args_list
            if "Starting server" in str(call)
        ]
        assert len(startup_calls) == 1
        assert "Starting server with log level" in str(startup_calls[0])
        assert "'INFO'" in str(startup_calls[0])

        # Check that shutdown message was logged
        shutdown_calls = [
            call
            for call in mock_logger.info.call_args_list
            if "Server stopped" in str(call)
        ]
        assert len(shutdown_calls) == 1

    def test_log_level_choices(self):
        """Test that valid log levels are accepted and invalid ones are rejected."""
        valid_levels = ["debug", "info", "warning", "error", "critical"]

        for level in valid_levels:
            with patch.object(
                sys, "argv", ["fabric-mcp", "--stdio", "--log-level", level]
            ):
                with patch("fabric_mcp.cli.FabricMCP"):
                    with patch("fabric_mcp.cli.Log"):
                        # Should not raise an exception
                        main()

        # Test invalid log level
        with patch.object(
            sys, "argv", ["fabric-mcp", "--stdio", "--log-level", "invalid"]
        ):
            with pytest.raises(SystemExit):
                main()

    def test_default_log_level_is_info(self):
        """Test that default log level is 'info'."""
        with (
            patch("fabric_mcp.cli.Log") as mock_log_class,
            patch("fabric_mcp.cli.FabricMCP") as mock_fabric_mcp_class,
        ):
            mock_log = Mock()
            mock_log.level_name = "INFO"
            mock_log.logger = Mock()
            mock_log_class.return_value = mock_log

            mock_fabric_mcp = Mock()
            mock_fabric_mcp_class.return_value = mock_fabric_mcp

            with patch.object(sys, "argv", ["fabric-mcp", "--stdio"]):
                main()

            # Verify default log level was used
            mock_log_class.assert_called_once_with("info")
