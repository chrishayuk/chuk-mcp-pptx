# Diagnostics Tools

This folder contains diagnostic and testing utilities for the PowerPoint MCP Server.

## Files

### Core Diagnostics
- **async_server.py** - Tests async server functionality
- **server_charts.py** - Tests chart creation through the server
- **chart_debug.py** - Debugging tool for chart creation issues
- **chart_utils.py** - Tests chart utility functions

### Compatibility Testing
- **compatibility.py** - Creates test files with increasing complexity
- **basic_pptx.py** - Basic python-pptx functionality test
- **minimal_issue.py** - Minimal reproduction of issues
- **minimal_chart_demo.py** - Minimal chart creation test

### File Validation
- **file_validity.py** - Validates PowerPoint file structure
- **xml_check.py** - Checks XML content in PowerPoint files

### Documentation
- **POWERPOINT_DIAGNOSTIC.md** - Detailed diagnostic report
- **KEYNOTE_COMPATIBILITY.md** - Keynote compatibility issues and solutions

## Usage

Run any diagnostic script with uv:

```bash
# Test async functionality
uv run python diagnostics/async_server.py

# Check file validity
uv run python diagnostics/file_validity.py

# Test compatibility
uv run python diagnostics/compatibility.py
```

## Output

All diagnostic outputs (.pptx files) are saved to the `../outputs/` directory.