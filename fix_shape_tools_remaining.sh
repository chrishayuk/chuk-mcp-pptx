#!/bin/bash

file="src/chuk_mcp_pptx/tools/shape_tools.py"

# Fix pptx_add_smart_art function
perl -i -p0e 's/        def _add_smart\(\):\n            prs = manager\.get\(presentation\)\n            if not prs:\n                return ErrorMessages\.NO_PRESENTATION\n            \n            if slide_index >= len\(prs\.slides\):\n                return f"Error: Slide index \{slide_index\} out of range"/        try:\n            result = await manager.get(presentation)\n            if not result:\n                return ErrorResponse(error=ErrorMessages.NO_PRESENTATION).model_dump_json()\n\n            prs, metadata = result\n\n            if slide_index >= len(prs.slides):\n                return ErrorResponse(\n                    error=f"Slide index {slide_index} not found in presentation"\n                ).model_dump_json()/s' "$file"

# Fix manager.update to await manager.update
perl -i -pe 's/(\s+)manager\.update\(presentation\)(?!\()/\1await manager.update(presentation)/g' "$file"

# Fix the return at end of _add_smart
perl -i -p0e 's/return await asyncio\.get_event_loop\(\)\.run_in_executor\(None, _add_smart\)/except Exception as e:\n            return ErrorResponse(error=f"Error adding SmartArt: {str(e)}").model_dump_json()/gs' "$file"

# Fix success return in _add_smart
perl -i -p0e 's/return f"Added \{art_type\} SmartArt with \{len\(items\)\} items to slide \{slide_index\}\{position_note\}"/message = f"Added {art_type} SmartArt with {len(items)} items to slide {slide_index}{position_note}"\n                return ComponentResponse(\n                    presentation=metadata.name,\n                    slide_index=slide_index,\n                    message=message,\n                    slide_count=metadata.slide_count\n                ).model_dump_json()/gs' "$file"

# Fix error return in try block
perl -i -p0e 's/return f"Error: Unsupported art type/return ErrorResponse(error=f"Unsupported art type/g' "$file"

echo "Fixed pptx_add_smart_art"
