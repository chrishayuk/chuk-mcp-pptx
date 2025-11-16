# chuk-mcp-pptx Examples

This directory contains working examples and debugging scripts for the chuk-mcp-pptx server.

## Working Examples

### 1. Basic Presentation (`basic_presentation.py`)
Direct library usage example - creates a presentation with title and content slides.

```bash
uv run python examples/basic_presentation.py
```

**Output:** `examples/output_basic.pptx` (29KB, 2 slides)

### 2. MCP Server Tools Test (`test_mcp_server.py`)
Tests all MCP tools directly without mcp-cli - verifies server functionality.

```bash
uv run python examples/test_mcp_server.py
```

**Output:** `examples/output_mcp_test.pptx` (28KB, 2 slides)

## Debugging Scripts

### 3. STDIO Mode Debug (`debug_stdio.py`)
Tests the server in stdio mode and checks internal state.

```bash
uv run python examples/debug_stdio.py
```

### 4. Server STDERR Capture (`test_server_stderr.py`)
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

- **VFS Provider "None"**: AsyncVirtualFileSystem lazy initialization working correctly
- **Server Crashes**: Run `test_mcp_server.py` first to isolate the issue
- **Missing Models**: Check `src/chuk_mcp_pptx/models/__init__.py` exports

## Expected Output

All examples should complete successfully:

```
✅ Success! Presentation created successfully.
📄 Output saved to: examples/output_*.pptx
```
