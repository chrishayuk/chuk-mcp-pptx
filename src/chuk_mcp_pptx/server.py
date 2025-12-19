#!/usr/bin/env python3
"""
PowerPoint MCP Server - Async-native implementation

This module provides the async MCP server for PowerPoint operations.
Supports both stdio (for Claude Desktop) and HTTP (for API access) transports.
"""

import logging
import os
import sys
from pathlib import Path

# Load environment variables from .env file
from dotenv import load_dotenv

# Find and load .env file from project root
env_path = Path(__file__).parent.parent.parent / ".env"
if env_path.exists():
    load_dotenv(env_path)

logger = logging.getLogger(__name__)


def _init_artifact_store() -> bool:
    """
    Initialize the artifact store from environment variables.

    Checks for S3/Tigris/filesystem configuration and sets up the global artifact store.
    This enables cloud storage or local filesystem for presentations.

    Returns:
        True if artifact store was initialized, False otherwise
    """
    # Check if we have storage configuration
    provider = os.environ.get("CHUK_ARTIFACTS_PROVIDER", "memory")
    bucket = os.environ.get("BUCKET_NAME")
    redis_url = os.environ.get("REDIS_URL")
    artifacts_path = os.environ.get("CHUK_ARTIFACTS_PATH")

    # For S3 provider, we need bucket and AWS credentials
    if provider == "s3":
        aws_key = os.environ.get("AWS_ACCESS_KEY_ID")
        aws_secret = os.environ.get("AWS_SECRET_ACCESS_KEY")
        aws_endpoint = os.environ.get("AWS_ENDPOINT_URL_S3")

        if not all([bucket, aws_key, aws_secret]):
            logger.warning(
                "S3 provider configured but missing credentials. "
                "Set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, and BUCKET_NAME."
            )
            return False

        logger.info(f"Initializing artifact store with S3 provider (bucket: {bucket})")
        logger.info(f"  Endpoint: {aws_endpoint}")
        logger.info(f"  Redis URL: {'configured' if redis_url else 'not configured'}")

    # For filesystem provider, ensure the directory exists
    elif provider == "filesystem":
        if artifacts_path:
            path_obj = Path(artifacts_path)
            path_obj.mkdir(parents=True, exist_ok=True)
            logger.info(
                f"Initializing artifact store with filesystem provider (path: {artifacts_path})"
            )
        else:
            logger.warning(
                "Filesystem provider configured but CHUK_ARTIFACTS_PATH not set. "
                "Defaulting to memory provider."
            )
            provider = "memory"

    try:
        from chuk_artifacts import ArtifactStore
        from chuk_mcp_server import set_global_artifact_store

        # Create the artifact store with environment-based configuration
        store_kwargs = {
            "storage_provider": provider,
            "session_provider": "redis" if redis_url else "memory",
        }

        # Add provider-specific kwargs
        if provider == "s3" and bucket:
            store_kwargs["bucket"] = bucket
        elif provider == "filesystem" and artifacts_path:
            # Note: chuk-artifacts may expect 'bucket' param for filesystem too
            store_kwargs["bucket"] = artifacts_path

        store = ArtifactStore(**store_kwargs)

        # Set as global artifact store for chuk-mcp-server context
        set_global_artifact_store(store)

        logger.info(f"Artifact store initialized successfully (provider: {provider})")
        return True

    except Exception as e:
        logger.error(f"Failed to initialize artifact store: {e}")
        return False


# Initialize artifact store at module load time
_artifact_store_ready = _init_artifact_store()

# Import mcp instance and all registered tools from async server
from .async_server import mcp  # noqa: F401, E402

# The tools are registered via decorators in their respective modules
# They become available as soon as the modules are imported by async_server


def main():
    """Main entry point for the MCP server.

    Automatically detects transport mode:
    - stdio: When stdin is piped or MCP_STDIO is set (for Claude Desktop)
    - HTTP: Default mode for API access
    """
    import argparse

    parser = argparse.ArgumentParser(description="PowerPoint MCP Server")
    parser.add_argument(
        "mode",
        nargs="?",
        choices=["stdio", "http"],
        default=None,
        help="Transport mode (stdio for Claude Desktop, http for API)",
    )
    parser.add_argument(
        "--host", default="localhost", help="Host for HTTP mode (default: localhost)"
    )
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP mode (default: 8000)")

    args = parser.parse_args()

    # Determine transport mode
    if args.mode == "stdio":
        # Explicitly requested stdio mode
        print("PowerPoint MCP Server starting in STDIO mode", file=sys.stderr)
        mcp.run(stdio=True)
    elif args.mode == "http":
        # Explicitly requested HTTP mode
        print(
            f"PowerPoint MCP Server starting in HTTP mode on {args.host}:{args.port}",
            file=sys.stderr,
        )
        mcp.run(host=args.host, port=args.port, stdio=False)
    else:
        # Auto-detect mode based on environment
        if os.environ.get("MCP_STDIO") or (not sys.stdin.isatty()):
            print("PowerPoint MCP Server starting in STDIO mode (auto-detected)", file=sys.stderr)
            mcp.run(stdio=True)
        else:
            print(
                f"PowerPoint MCP Server starting in HTTP mode on {args.host}:{args.port}",
                file=sys.stderr,
            )
            mcp.run(host=args.host, port=args.port, stdio=False)


if __name__ == "__main__":
    main()
