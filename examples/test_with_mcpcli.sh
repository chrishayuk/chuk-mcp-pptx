#!/bin/bash
# Test chuk-mcp-pptx with mcp-cli in verbose mode
# This script runs mcp-cli with a test command and captures all output

set -e

echo "🧪 Testing chuk-mcp-pptx with mcp-cli in verbose mode"
echo ""

# Go to mcp-cli directory
cd /Users/christopherhay/chris-source/mcp-cli

# Run mcp-cli with verbose logging and a simple test command
# We'll use a here-doc to send commands
echo "Running: uv run mcp-cli --server powerpoint --provider openai --model gpt-5-mini --verbose --log-level DEBUG"
echo ""

# Send a simple command and then exit
(
  sleep 1
  echo "create a simple presentation called test"
  sleep 2
  echo "exit"
) | timeout 10 uv run mcp-cli --server powerpoint --provider openai --model gpt-5-mini --verbose --log-level DEBUG 2>&1 | tee /tmp/mcpcli_debug.log

echo ""
echo "📄 Full log saved to: /tmp/mcpcli_debug.log"
echo ""
echo "🔍 Searching for errors in log..."
grep -i "error\|exception\|traceback\|crash\|failed" /tmp/mcpcli_debug.log || echo "No obvious errors found"
