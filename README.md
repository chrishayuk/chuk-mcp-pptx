# Chuk MCP PowerPoint Server

An MCP server for PowerPoint operations using python-pptx, built with the chuk-mcp-server framework.

## Project Structure

```
chuk-mcp-pptx/
├── src/chuk_mcp_pptx/     # Main package (async-native server)
├── examples/              # Example scripts and demos
├── diagnostics/           # Testing and diagnostic tools  
├── outputs/               # Generated PowerPoint files
└── tests/                 # Unit tests
```

## Features

- Create and manage multiple PowerPoint presentations
- Add various slide types (title, content, text, images)
- Save/load presentations to/from disk
- Import/export presentations as base64 for easy transfer
- **Virtual Filesystem Integration** - Optional VFS persistence for multi-server scenarios
- **Scalable Architecture** - No global state, proper encapsulation with PresentationManager
- **Auto-save to VFS** - Presentations automatically persist to VFS when enabled

## Installation

```bash
# Using uv
uv sync
uv run chuk-mcp-pptx

# Or using pip
pip install -e .
```

## Usage

The server provides the following MCP tools:

### Presentation Management
- `pptx_create` - Create a new presentation
- `pptx_list` - List all open presentations
- `pptx_switch` - Switch between presentations
- `pptx_get_info` - Get detailed info about a presentation
- `pptx_close` - Close a presentation
- `pptx_clear_all` - Clear all presentations from memory
- `pptx_status` - Get server status and VFS configuration

### Slide Operations
- `pptx_add_title_slide` - Add a title slide
- `pptx_add_slide` - Add a content slide with bullet points
- `pptx_add_text_slide` - Add a slide with text content
- `pptx_add_image_slide` - Add a slide with an image

### File Operations
- `pptx_save` - Save presentation to disk
- `pptx_load` - Load presentation from disk
- `pptx_export_base64` - Export as base64 data
- `pptx_import_base64` - Import from base64 data

## Running the Server

The server can run in different transport modes:

```bash
# Auto-detect mode (stdio for Claude Desktop, HTTP otherwise)
uv run python -m chuk_mcp_pptx.server

# Force stdio mode
MCP_TRANSPORT=stdio uv run python -m chuk_mcp_pptx.server

# Force HTTP mode on specific port
MCP_TRANSPORT=http MCP_PORT=8080 uv run python -m chuk_mcp_pptx.server

# Enable VFS persistence mode
PPTX_USE_VFS=true uv run python -m chuk_mcp_pptx.server

# VFS mode with custom path
PPTX_USE_VFS=true PPTX_VFS_PATH="vfs://my-presentations" uv run python -m chuk_mcp_pptx.server
```

### Environment Variables

- `PPTX_USE_VFS`: Set to "true" to enable VFS persistence (default: "false")
- `PPTX_VFS_PATH`: Base path in VFS for storing presentations (default: "vfs://presentations")

## Integration with Virtual Shell/Filesystem

The server supports multiple integration patterns:

1. **Direct file operations**: Save/load presentations directly to/from disk
2. **Base64 transfer**: Export/import presentations as base64 for transfer via virtual shell
3. **Image support**: Add images via file path or base64 data URLs

## Example Usage

When connected via MCP, tools can be called like:

```python
# Create a presentation
pptx_create(name="quarterly_report")

# Add a title slide
pptx_add_title_slide(
    title="Q4 2024 Results",
    subtitle="Revenue and Growth Analysis"
)

# Add content slide with bullets
pptx_add_slide(
    title="Key Achievements",
    content=[
        "Revenue increased by 25%",
        "Launched 3 new products",
        "Expanded to 5 new markets"
    ]
)

# Save the presentation
pptx_save(path="q4_report.pptx")

# Export for transfer
pptx_export_base64()  # Returns base64 data
```

## MCP Configuration

For Claude Desktop, add to your MCP settings:

```json
{
  "mcpServers": {
    "chuk-mcp-pptx": {
      "command": "uv",
      "args": ["run", "python", "-m", "chuk_mcp_pptx.server"],
      "cwd": "/path/to/chuk-mcp-pptx"
    }
  }
}
```

## Testing

Run the test suite:

```bash
uv run python tests/test_tools.py
```

## Dependencies

- `python-pptx` - PowerPoint file creation and manipulation
- `chuk-mcp-server` - MCP server framework
- `mcp` - Model Context Protocol implementation