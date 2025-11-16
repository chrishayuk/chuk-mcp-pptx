#!/usr/bin/env python3
"""Fix slide_layout_tools.py async patterns"""

import re

file_path = "src/chuk_mcp_pptx/tools/slide_layout_tools.py"

with open(file_path, 'r') as f:
    content = f.read()

# Pattern 1: Replace def _func(): with try:
content = re.sub(
    r'        def (_\w+)\(\):\n            prs = manager\.get\(presentation\)\n            if not prs:\n                return ErrorMessages\.NO_PRESENTATION',
    r'''        try:
            result = await manager.get(presentation)
            if not result:
                return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()

            prs, metadata = result''',
    content
)

# Pattern 2: Replace manager.update(presentation) with await manager.update(presentation)
content = re.sub(
    r'(\s+)manager\.update\(presentation\)(?!\()',
    r'\1await manager.update(presentation)',
    content
)

# Pattern 3: Replace return await asyncio.get_event_loop().run_in_executor(None, _func) with exception handler
content = re.sub(
    r'        return await asyncio\.get_event_loop\(\)\.run_in_executor\(None, _\w+\)',
    r'        except Exception as e:\n            return ErrorResponse(error=str(e)).model_dump_json()',
    content
)

# Pattern 4: Update slide index error messages
content = re.sub(
    r'return f"Error: Slide index \{slide_index\} out of range',
    r'return ErrorResponse(error=f"Slide index {slide_index} not found in presentation',
    content
)

# Pattern 5: Update simple error returns to use ErrorResponse
content = re.sub(
    r'return "Error: ([^"]+)"',
    r'return ErrorResponse(error="\1").model_dump_json()',
    content
)

# Pattern 6: Update simple success returns to use SuccessResponse
content = re.sub(
    r'return f"([^"]*)\{([^}]+)\}([^"]*)"(?!\s*\))',
    lambda m: f'return SuccessResponse(message=f"{m.group(1)}{{{m.group(2)}}}{m.group(3)}").model_dump_json()',
    content
)

with open(file_path, 'w') as f:
    f.write(content)

print("Fixed slide_layout_tools.py")
