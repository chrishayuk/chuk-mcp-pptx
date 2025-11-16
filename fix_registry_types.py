#!/usr/bin/env python3
"""Fix type hints in registry.py"""

import re

file_path = "src/chuk_mcp_pptx/registry.py"

with open(file_path, 'r') as f:
    content = f.read()

# Replace List[ with list[
content = re.sub(r'\bList\[', 'list[', content)

# Replace Dict[ with dict[
content = re.sub(r'\bDict\[', 'dict[', content)

with open(file_path, 'w') as f:
    f.write(content)

print("Updated registry.py with modern type hints")
