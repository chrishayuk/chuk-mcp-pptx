#!/usr/bin/env python3
"""
Artifact Storage Example for PowerPoint MCP Server

This example demonstrates how chuk-mcp-pptx integrates with chuk-artifacts
for persistent storage. It shows:

1. Creating presentations with automatic artifact storage
2. Retrieving artifact URIs and namespace IDs
3. Exporting presentations with artifact metadata
4. Using the ArtifactStore directly for advanced operations

The integration uses chuk-mcp-server's built-in artifact store context,
which provides session-scoped storage with support for multiple backends
(memory, filesystem, sqlite, s3).
"""

import asyncio
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from chuk_artifacts import ArtifactStore
from chuk_mcp_server import set_global_artifact_store

from chuk_mcp_pptx.presentation_manager import PresentationManager


async def main():
    """Demonstrate artifact storage integration."""
    print("=" * 60)
    print("PowerPoint MCP Server - Artifact Storage Example")
    print("=" * 60)

    # =================================================================
    # STEP 1: Initialize the Artifact Store
    # =================================================================
    print("\n1. Initializing ArtifactStore...")

    # Create an artifact store with memory provider (for demo)
    # In production, you might use "vfs-filesystem", "vfs-sqlite", or "vfs-s3"
    store = ArtifactStore()

    # Set it as the global artifact store for chuk-mcp-server context
    # This makes it available to PresentationManager via get_artifact_store()
    set_global_artifact_store(store)
    print("   ArtifactStore initialized with memory provider")

    # =================================================================
    # STEP 2: Create a PresentationManager
    # =================================================================
    print("\n2. Creating PresentationManager...")

    manager = PresentationManager(base_path="presentations")
    print(f"   Base path: {manager.base_path}")
    print(f"   MIME type: {manager.PPTX_MIME_TYPE}")

    # =================================================================
    # STEP 3: Create a presentation (automatically stored as artifact)
    # =================================================================
    print("\n3. Creating presentation...")

    metadata = await manager.create(name="quarterly_report", theme="dark")

    print(f"   Name: {metadata.name}")
    print(f"   Slide count: {metadata.slide_count}")
    print(f"   Theme: {metadata.theme}")
    print(f"   Namespace ID: {metadata.namespace_id}")
    print(f"   Artifact URI: {metadata.vfs_path}")
    print(f"   Is saved: {metadata.is_saved}")

    # =================================================================
    # STEP 4: Add content to the presentation
    # =================================================================
    print("\n4. Adding slides to presentation...")

    # Get the presentation object
    result = await manager.get("quarterly_report")
    if result:
        prs, meta = result

        # Add a title slide
        title_layout = prs.slide_layouts[0]  # Title slide layout
        slide = prs.slides.add_slide(title_layout)
        title = slide.shapes.title
        subtitle = slide.placeholders[1]
        title.text = "Q4 2024 Report"
        subtitle.text = "Company Performance Overview"

        # Add a content slide
        content_layout = prs.slide_layouts[1]  # Title and content layout
        slide2 = prs.slides.add_slide(content_layout)
        slide2.shapes.title.text = "Key Metrics"

        # Update the presentation in the artifact store
        await manager.update("quarterly_report")

        print(f"   Added {len(prs.slides)} slides")
        print("   Presentation updated in artifact store")

    # =================================================================
    # STEP 5: Retrieve artifact information
    # =================================================================
    print("\n5. Retrieving artifact information...")

    namespace_id = manager.get_namespace_id("quarterly_report")
    artifact_uri = manager.get_artifact_uri("quarterly_report")

    print(f"   Namespace ID: {namespace_id}")
    print(f"   Artifact URI: {artifact_uri}")

    # =================================================================
    # STEP 6: Export as base64 with artifact metadata
    # =================================================================
    print("\n6. Exporting presentation...")

    base64_data = await manager.export_base64("quarterly_report")
    if base64_data:
        print(f"   Export size: {len(base64_data)} bytes (base64)")
        print(f"   MIME type: {manager.PPTX_MIME_TYPE}")

    # =================================================================
    # STEP 7: List all presentations
    # =================================================================
    print("\n7. Listing all presentations...")

    list_response = await manager.list_presentations()
    print(f"   Total presentations: {list_response.total}")
    print(f"   Current presentation: {list_response.current}")

    for pres_info in list_response.presentations:
        print(f"\n   Presentation: {pres_info.name}")
        print(f"     Slides: {pres_info.slide_count}")
        print(f"     Is current: {pres_info.is_current}")
        print(f"     Namespace ID: {pres_info.namespace_id}")
        print(f"     Artifact URI: {pres_info.file_path}")

    # =================================================================
    # STEP 8: Create a second presentation
    # =================================================================
    print("\n8. Creating second presentation...")

    metadata2 = await manager.create(name="project_update", theme="light")
    print(f"   Created: {metadata2.name}")
    print(f"   Namespace ID: {metadata2.namespace_id}")

    # =================================================================
    # STEP 9: Switch between presentations
    # =================================================================
    print("\n9. Switching presentations...")

    await manager.set_current("quarterly_report")
    print(f"   Current: {manager.get_current_name()}")

    await manager.set_current("project_update")
    print(f"   Switched to: {manager.get_current_name()}")

    # =================================================================
    # STEP 10: Direct artifact store operations (advanced)
    # =================================================================
    print("\n10. Direct artifact store operations...")

    # You can also access the artifact store directly for advanced operations
    # such as checkpoints, listing namespaces, or custom metadata

    # Create a checkpoint of the current presentation
    ns_id = manager.get_namespace_id("quarterly_report")
    if ns_id:
        try:
            checkpoint = await store.checkpoint_namespace(ns_id, name="v1.0")
            print(f"   Created checkpoint: {checkpoint.name}")
            print(f"   Checkpoint ID: {checkpoint.checkpoint_id}")
        except Exception as e:
            print(f"   Checkpoint not available: {e}")

    # =================================================================
    # STEP 11: Clean up
    # =================================================================
    print("\n11. Cleaning up...")

    await manager.delete("project_update")
    print("   Deleted: project_update")

    # List remaining presentations
    list_response = await manager.list_presentations()
    print(f"   Remaining presentations: {list_response.total}")

    # =================================================================
    # Summary
    # =================================================================
    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)
    print("""
The chuk-mcp-pptx server integrates with chuk-artifacts to provide:

1. Automatic persistence - Presentations are automatically saved
   to the artifact store when created or modified.

2. Session scoping - Each session gets isolated storage, preventing
   conflicts between concurrent users.

3. Artifact URIs - Every presentation gets a unique URI that can be
   used to reference it across the system.

4. Namespace IDs - Internal identifiers for direct artifact store
   operations like checkpoints and metadata queries.

5. Multiple backends - The same code works with memory, filesystem,
   SQLite, or S3 storage by changing the provider configuration.

6. Base64 export - Presentations can be exported as base64 for
   transmission over APIs or storage in databases.
""")
    print("Example completed successfully!")


async def demo_with_mcp_server_context():
    """
    Alternative demo showing usage within an MCP server context.

    When running as part of an MCP server, the artifact store is
    automatically set up by chuk-mcp-server's context management.
    """
    print("\n" + "=" * 60)
    print("MCP Server Context Demo")
    print("=" * 60)

    # In a real MCP server, you would use RequestContext:
    #
    # from chuk_mcp_server import RequestContext, set_artifact_store
    #
    # async with RequestContext(session_id="session-123", user_id="user-456"):
    #     set_artifact_store(store)
    #
    #     # Now all tools in this context can use the artifact store
    #     manager = PresentationManager()
    #     await manager.create("my_presentation")
    #
    # The presentation will be stored in the session-scoped namespace,
    # ensuring isolation from other users and sessions.

    print("""
In an MCP server context:

1. The server sets up the artifact store during initialization
2. Each request gets a RequestContext with session/user info
3. PresentationManager automatically uses the context's artifact store
4. Storage is scoped to the session for isolation
5. No manual store initialization needed in tool handlers
""")


if __name__ == "__main__":
    print("\nPowerPoint MCP Server - Artifact Storage Integration")
    print("Using chuk-artifacts for persistent presentation storage\n")

    asyncio.run(main())
    asyncio.run(demo_with_mcp_server_context())
