#!/usr/bin/env python3
"""Fix type hints in all remaining files"""

import re

files = [
    "src/chuk_mcp_pptx/chart_tools.py",
    "src/chuk_mcp_pptx/composition.py",
    "src/chuk_mcp_pptx/inspection_tools.py",
    "src/chuk_mcp_pptx/variants.py",
]

for file_path in files:
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        
        # Check if __future__ import already exists
        if 'from __future__ import annotations' not in content:
            # Find the first import or after docstring
            if content.startswith('"""'):
                # Find end of docstring
                end_doc = content.find('"""', 3) + 3
                # Insert after docstring
                before = content[:end_doc]
                after = content[end_doc:]
                content = before + '\nfrom __future__ import annotations\n' + after
            else:
                # Insert at beginning
                content = 'from __future__ import annotations\n\n' + content
        
        # Replace Optional[T] with T | None
        content = re.sub(r'Optional\[([^\]]+)\]', r'\1 | None', content)
        
        # Replace List[ with list[
        content = re.sub(r'\bList\[', 'list[', content)
        
        # Replace Dict[ with dict[
        content = re.sub(r'\bDict\[', 'dict[', content)
        
        # Replace Tuple[ with tuple[
        content = re.sub(r'\bTuple\[', 'tuple[', content)
        
        # Replace Set[ with set[
        content = re.sub(r'\bSet\[', 'set[', content)
        
        with open(file_path, 'w') as f:
            f.write(content)
        
        print(f"✓ Updated {file_path}")
    except Exception as e:
        print(f"✗ Error updating {file_path}: {e}")

print("\nAll files updated with modern type hints!")
