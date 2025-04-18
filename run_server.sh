#!/bin/bash
# Wrapper script to run the YouTube MCP server

# Get the directory where the script resides
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Define the path to the virtual environment relative to the script
VENV_DIR="$SCRIPT_DIR/.venv"

# Define the path to the Python executable within the venv
PYTHON_EXEC="$VENV_DIR/bin/python"

# Define the path to the server script relative to the script
SERVER_SCRIPT="$SCRIPT_DIR/youtube_server.py"

# Check if the Python executable exists
if [ ! -f "$PYTHON_EXEC" ]; then
    echo "Error: Python executable not found at $PYTHON_EXEC"
    echo "Please ensure you have created the virtual environment using 'uv venv' in the $SCRIPT_DIR directory."
    exit 1
fi

# Check if the server script exists
if [ ! -f "$SERVER_SCRIPT" ]; then
    echo "Error: Server script not found at $SERVER_SCRIPT"
    exit 1
fi

# Execute the server script using the venv Python
echo "Starting YouTube MCP server using $PYTHON_EXEC..."
"$PYTHON_EXEC" "$SERVER_SCRIPT" "$@" # Pass any arguments through 