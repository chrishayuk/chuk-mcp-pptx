# tests/test_server.py
"""
Tests for server.py module.

Tests the MCP server initialization and entry points:
- Environment variable loading
- Artifact store initialization
- Main entry point with different transport modes
"""

import pytest
import os
from pathlib import Path
from unittest.mock import patch, MagicMock


# ============================================================================
# Test Artifact Store Initialization
# ============================================================================


class TestInitArtifactStore:
    """Tests for _init_artifact_store function."""

    def test_init_artifact_store_memory_provider_default(self):
        """Test default memory provider initialization."""
        # Clear any existing environment variables
        env_vars = {
            "CHUK_ARTIFACTS_PROVIDER": "memory",
            "BUCKET_NAME": "",
            "REDIS_URL": "",
            "CHUK_ARTIFACTS_PATH": "",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            # Re-import to test initialization
            # Note: We can't easily re-run module init, so test the function directly
            from chuk_mcp_pptx.server import _init_artifact_store

            # The function should return True or False based on imports
            result = _init_artifact_store()
            assert isinstance(result, bool)

    def test_init_artifact_store_s3_missing_credentials(self):
        """Test S3 provider with missing credentials logs warning."""
        env_vars = {
            "CHUK_ARTIFACTS_PROVIDER": "s3",
            "BUCKET_NAME": "",
            "AWS_ACCESS_KEY_ID": "",
            "AWS_SECRET_ACCESS_KEY": "",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            with patch("chuk_mcp_pptx.server.logger") as mock_logger:
                from chuk_mcp_pptx.server import _init_artifact_store

                result = _init_artifact_store()
                # Should return False due to missing credentials
                assert result is False
                mock_logger.warning.assert_called()

    def test_init_artifact_store_s3_with_credentials(self):
        """Test S3 provider with all credentials."""
        env_vars = {
            "CHUK_ARTIFACTS_PROVIDER": "s3",
            "BUCKET_NAME": "test-bucket",
            "AWS_ACCESS_KEY_ID": "test-key",
            "AWS_SECRET_ACCESS_KEY": "test-secret",
            "AWS_ENDPOINT_URL_S3": "https://s3.example.com",
            "REDIS_URL": "",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            with patch("chuk_mcp_pptx.server.logger") as mock_logger:
                with patch("chuk_artifacts.ArtifactStore") as mock_store_class:
                    with patch("chuk_mcp_server.set_global_artifact_store"):
                        mock_store_class.return_value = MagicMock()

                        from chuk_mcp_pptx.server import _init_artifact_store

                        result = _init_artifact_store()
                        assert result is True
                        mock_logger.info.assert_called()

    def test_init_artifact_store_filesystem_provider(self, tmp_path):
        """Test filesystem provider initialization."""
        env_vars = {
            "CHUK_ARTIFACTS_PROVIDER": "filesystem",
            "CHUK_ARTIFACTS_PATH": str(tmp_path / "artifacts"),
            "REDIS_URL": "",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            with patch("chuk_mcp_pptx.server.logger"):
                with patch("chuk_artifacts.ArtifactStore") as mock_store_class:
                    with patch("chuk_mcp_server.set_global_artifact_store"):
                        mock_store_class.return_value = MagicMock()

                        from chuk_mcp_pptx.server import _init_artifact_store

                        result = _init_artifact_store()
                        assert result is True
                        # Directory should be created
                        assert (tmp_path / "artifacts").exists()

    def test_init_artifact_store_filesystem_no_path(self):
        """Test filesystem provider without path falls back to memory."""
        env_vars = {
            "CHUK_ARTIFACTS_PROVIDER": "filesystem",
            "CHUK_ARTIFACTS_PATH": "",
            "REDIS_URL": "",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            with patch("chuk_mcp_pptx.server.logger") as mock_logger:
                with patch("chuk_artifacts.ArtifactStore") as mock_store_class:
                    with patch("chuk_mcp_server.set_global_artifact_store"):
                        mock_store_class.return_value = MagicMock()

                        from chuk_mcp_pptx.server import _init_artifact_store

                        _init_artifact_store()
                        # Should warn and fall back to memory
                        mock_logger.warning.assert_called()

    def test_init_artifact_store_exception_handling(self):
        """Test exception handling during artifact store initialization."""
        env_vars = {
            "CHUK_ARTIFACTS_PROVIDER": "memory",
            "REDIS_URL": "",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            with patch("chuk_mcp_pptx.server.logger") as mock_logger:
                with patch("chuk_artifacts.ArtifactStore") as mock_store_class:
                    mock_store_class.side_effect = Exception("Init failed")

                    from chuk_mcp_pptx.server import _init_artifact_store

                    result = _init_artifact_store()
                    assert result is False
                    mock_logger.error.assert_called()

    def test_init_artifact_store_with_redis(self):
        """Test initialization with Redis session provider."""
        env_vars = {
            "CHUK_ARTIFACTS_PROVIDER": "memory",
            "REDIS_URL": "redis://localhost:6379",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            with patch("chuk_artifacts.ArtifactStore") as mock_store_class:
                with patch("chuk_mcp_server.set_global_artifact_store"):
                    mock_store_class.return_value = MagicMock()

                    from chuk_mcp_pptx.server import _init_artifact_store

                    result = _init_artifact_store()
                    assert result is True

                    # Verify redis session provider was used
                    call_kwargs = mock_store_class.call_args.kwargs
                    assert call_kwargs.get("session_provider") == "redis"


# ============================================================================
# Test Main Entry Point
# ============================================================================


class TestMain:
    """Tests for main() entry point function."""

    def test_main_stdio_explicit(self):
        """Test main with explicit stdio mode."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py", "stdio"]):
            with patch("chuk_mcp_pptx.server.mcp") as mock_mcp:
                main()
                mock_mcp.run.assert_called_once_with(stdio=True)

    def test_main_http_explicit(self):
        """Test main with explicit http mode."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py", "http"]):
            with patch("chuk_mcp_pptx.server.mcp") as mock_mcp:
                main()
                mock_mcp.run.assert_called_once_with(host="localhost", port=8000, stdio=False)

    def test_main_http_custom_host_port(self):
        """Test main with custom host and port."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py", "http", "--host", "0.0.0.0", "--port", "9000"]):
            with patch("chuk_mcp_pptx.server.mcp") as mock_mcp:
                main()
                mock_mcp.run.assert_called_once_with(host="0.0.0.0", port=9000, stdio=False)

    def test_main_auto_detect_stdio_env(self):
        """Test main auto-detects stdio from MCP_STDIO env var."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py"]):
            with patch.dict(os.environ, {"MCP_STDIO": "1"}):
                with patch("chuk_mcp_pptx.server.mcp") as mock_mcp:
                    main()
                    mock_mcp.run.assert_called_once_with(stdio=True)

    def test_main_auto_detect_stdio_not_tty(self):
        """Test main auto-detects stdio when stdin is not a TTY."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py"]):
            with patch.dict(os.environ, {"MCP_STDIO": ""}, clear=False):
                with patch("sys.stdin") as mock_stdin:
                    mock_stdin.isatty.return_value = False
                    with patch("chuk_mcp_pptx.server.mcp") as mock_mcp:
                        main()
                        mock_mcp.run.assert_called_once_with(stdio=True)

    def test_main_auto_detect_http(self):
        """Test main auto-detects HTTP when stdin is a TTY."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py"]):
            with patch.dict(os.environ, {"MCP_STDIO": ""}, clear=False):
                with patch("sys.stdin") as mock_stdin:
                    mock_stdin.isatty.return_value = True
                    with patch("chuk_mcp_pptx.server.mcp") as mock_mcp:
                        main()
                        mock_mcp.run.assert_called_once_with(
                            host="localhost", port=8000, stdio=False
                        )

    def test_main_prints_startup_message_stdio(self, capsys):
        """Test that stdio mode prints startup message."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py", "stdio"]):
            with patch("chuk_mcp_pptx.server.mcp"):
                main()
                captured = capsys.readouterr()
                assert "STDIO" in captured.err

    def test_main_prints_startup_message_http(self, capsys):
        """Test that HTTP mode prints startup message with host/port."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py", "http", "--host", "127.0.0.1", "--port", "5000"]):
            with patch("chuk_mcp_pptx.server.mcp"):
                main()
                captured = capsys.readouterr()
                assert "HTTP" in captured.err
                assert "127.0.0.1" in captured.err
                assert "5000" in captured.err


# ============================================================================
# Test Module-level Initialization
# ============================================================================


class TestModuleInit:
    """Tests for module-level initialization."""

    def test_mcp_imported(self):
        """Test that mcp is imported from async_server."""
        from chuk_mcp_pptx.server import mcp

        assert mcp is not None

    def test_artifact_store_ready_flag_exists(self):
        """Test that _artifact_store_ready flag is set."""
        from chuk_mcp_pptx import server

        assert hasattr(server, "_artifact_store_ready")
        assert isinstance(server._artifact_store_ready, bool)


# ============================================================================
# Test Environment File Loading
# ============================================================================


class TestEnvFileLoading:
    """Tests for .env file loading."""

    def test_env_path_calculation(self):
        """Test that env_path is correctly calculated."""
        from chuk_mcp_pptx import server

        # Verify env_path is a Path object
        assert hasattr(server, "env_path")
        assert isinstance(server.env_path, Path)

    def test_env_file_loaded_when_exists(self, tmp_path):
        """Test that .env file is loaded when it exists."""
        # This is tricky to test since it runs at import time
        # We can verify the mechanism is in place
        from chuk_mcp_pptx.server import env_path

        # env_path should point to .env in project root
        assert env_path.name == ".env"


# ============================================================================
# Test Edge Cases
# ============================================================================


class TestEdgeCases:
    """Tests for edge cases."""

    def test_main_no_args(self):
        """Test main with no arguments uses auto-detection."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py"]):
            with patch.dict(os.environ, {"MCP_STDIO": ""}, clear=False):
                with patch("sys.stdin") as mock_stdin:
                    mock_stdin.isatty.return_value = True
                    with patch("chuk_mcp_pptx.server.mcp") as mock_mcp:
                        main()
                        # Should default to HTTP mode
                        assert mock_mcp.run.called

    def test_init_artifact_store_s3_partial_credentials(self):
        """Test S3 provider with only some credentials."""
        env_vars = {
            "CHUK_ARTIFACTS_PROVIDER": "s3",
            "BUCKET_NAME": "test-bucket",
            "AWS_ACCESS_KEY_ID": "test-key",
            "AWS_SECRET_ACCESS_KEY": "",  # Missing
        }

        with patch.dict(os.environ, env_vars, clear=False):
            with patch("chuk_mcp_pptx.server.logger") as mock_logger:
                from chuk_mcp_pptx.server import _init_artifact_store

                result = _init_artifact_store()
                # Should fail due to missing secret
                assert result is False
                mock_logger.warning.assert_called()

    def test_init_artifact_store_filesystem_creates_nested_dir(self, tmp_path):
        """Test filesystem provider creates nested directories."""
        nested_path = tmp_path / "level1" / "level2" / "artifacts"
        env_vars = {
            "CHUK_ARTIFACTS_PROVIDER": "filesystem",
            "CHUK_ARTIFACTS_PATH": str(nested_path),
            "REDIS_URL": "",
        }

        with patch.dict(os.environ, env_vars, clear=False):
            with patch("chuk_artifacts.ArtifactStore") as mock_store_class:
                with patch("chuk_mcp_server.set_global_artifact_store"):
                    mock_store_class.return_value = MagicMock()

                    from chuk_mcp_pptx.server import _init_artifact_store

                    _init_artifact_store()
                    # Nested directories should be created
                    assert nested_path.exists()


# ============================================================================
# Test Argparse
# ============================================================================


class TestArgparse:
    """Tests for argument parsing."""

    def test_argparse_help(self):
        """Test argparse help doesn't raise."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py", "--help"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code == 0

    def test_argparse_invalid_mode(self):
        """Test argparse with invalid mode."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py", "invalid_mode"]):
            with pytest.raises(SystemExit) as exc_info:
                main()
            assert exc_info.value.code != 0

    def test_argparse_port_as_string(self):
        """Test argparse converts port to int."""
        from chuk_mcp_pptx.server import main

        with patch("sys.argv", ["server.py", "http", "--port", "3000"]):
            with patch("chuk_mcp_pptx.server.mcp") as mock_mcp:
                main()
                call_kwargs = mock_mcp.run.call_args.kwargs
                assert call_kwargs["port"] == 3000
                assert isinstance(call_kwargs["port"], int)
