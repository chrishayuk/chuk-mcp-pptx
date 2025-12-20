# chuk-mcp-pptx Examples

This directory contains working examples and debugging scripts for the chuk-mcp-pptx server.

## Golden Path Examples

These examples demonstrate the **optimal workflow** for generating professional presentations. Use these as reference for demos, videos, and LLM agent development.

### Golden Path: Pitch Deck (`golden_path_pitch_deck.py`)

The canonical example showing the ideal template-first workflow for an 8-slide startup pitch deck.

```bash
uv run python examples/golden_path_pitch_deck.py
```

**Key concepts demonstrated:**
- Template analysis before building slides
- Using layout variety (not repeating the same layout)
- Placeholder population with text and structured content
- Verification with `pptx_list_slide_components`

**Output:** `examples/output_pitch_deck.pptx` (8 slides)

### Golden Path Prompts (`GOLDEN_PATH_PROMPTS.md`)

Documentation with three canonical demo prompts and expected tool-call sequences:
1. **Startup Pitch Deck** (8 slides) - Full workflow example
2. **Quarterly Business Review** (10 slides) - Charts and tables
3. **Technical Tutorial** (6 slides) - Code examples and diagrams

Also includes common mistakes to avoid and a layout selection guide.

---

## Working Examples

### 1. Artifact Storage Integration (`artifact_storage_example.py`)
Demonstrates the chuk-artifacts integration for persistent presentation storage.

```bash
uv run python examples/artifact_storage_example.py
```

**Features demonstrated:**
- Creating presentations with automatic artifact storage
- Retrieving artifact URIs and namespace IDs
- Exporting presentations with artifact metadata
- Direct artifact store operations (checkpoints)
- Session-scoped storage isolation

### 2. Basic Presentation (`basic_presentation.py`)
Direct library usage example - creates a presentation with title and content slides.

```bash
uv run python examples/basic_presentation.py
```

**Output:** `examples/output_basic.pptx` (29KB, 2 slides)

### 3. MCP Server Tools Test (`test_mcp_server.py`)
Tests all MCP tools directly without mcp-cli - verifies server functionality.

```bash
uv run python examples/test_mcp_server.py
```

**Output:** `examples/output_mcp_test.pptx` (28KB, 2 slides)

## Debugging Scripts

### 4. STDIO Mode Debug (`debug_stdio.py`)
Tests the server in stdio mode and checks internal state.

```bash
uv run python examples/debug_stdio.py
```

### 5. Server STDERR Capture (`test_server_stderr.py`)
Runs the actual MCP server with detailed logging to help debug crashes.

```bash
uv run python examples/test_server_stderr.py
```

Then in another terminal, connect with mcp-cli:
```bash
cd /path/to/mcp-cli
uv run mcp-cli --server powerpoint --provider openai --model gpt-5-min
```

The first terminal will show all server logs and errors.

## Common Issues

- **Artifact Store Not Available**: The server gracefully handles missing artifact stores by keeping presentations in memory only
- **Server Crashes**: Run `test_mcp_server.py` first to isolate the issue
- **Missing Models**: Check `src/chuk_mcp_pptx/models/__init__.py` exports

## Storage Architecture

The server uses chuk-artifacts for persistent storage:

```
PresentationManager
    │
    └── ArtifactStore (from chuk-mcp-server context)
            │
            └── Storage Backends
                ├── memory (default, fast, ephemeral)
                ├── filesystem (local files)
                ├── sqlite (embedded database)
                └── s3 (cloud storage)
```

Each presentation is stored as a BLOB namespace with:
- Automatic session scoping
- MIME type metadata
- Checkpoint support
- Artifact URIs for reference

## Expected Output

All examples should complete successfully:

```
✅ Success! Presentation created successfully.
📄 Output saved to: examples/output_*.pptx
```
