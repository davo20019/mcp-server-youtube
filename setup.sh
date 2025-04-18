#!/bin/bash

# Simple setup script for the MCP YouTube Server
# Run this from within the mcp-server-youtube directory after cloning.

set -e # Exit immediately if a command exits with a non-zero status.

# PROJECT_DIR="mcp-server-youtube" # No longer needed as we run from within

echo "Starting MCP YouTube Server setup (running from $(pwd))..."

# 1. Check if required files exist (basic sanity check)
if [ ! -f "pyproject.toml" ] || [ ! -f "run_server.sh" ]; then
    echo "Error: Missing pyproject.toml or run_server.sh."
    echo "Please ensure you are running this script from within the 'mcp-server-youtube' directory."
    exit 1
fi

# Change into the project directory # No longer needed
# cd "$PROJECT_DIR"
# echo "Changed directory to $(pwd)"

# 2. Check for uv
if ! command -v uv &> /dev/null; then
    echo "Error: 'uv' command not found."
    echo "Please install uv first. See: https://github.com/astral-sh/uv"
    exit 1
fi
echo "'uv' command found."

# 3. Create virtual environment
echo "Creating Python virtual environment using 'uv venv'..."
uv venv

# 4. Install dependencies
echo "Installing dependencies using 'uv sync' (this might take a moment)..."
uv sync

# 5. Configure .env file
read -p "Enter your YouTube Data API v3 Key: " YOUTUBE_API_KEY
if [ -z "$YOUTUBE_API_KEY" ]; then
    echo "Warning: No API key provided. Creating .env file without a key."
    echo "You will need to manually edit the '.env' file later and add your key."
    YOUTUBE_API_KEY="YOUR_API_KEY_HERE"
fi

# Create or overwrite .env file
echo "Creating/updating .env file..."
echo "YOUTUBE_API_KEY=$YOUTUBE_API_KEY" > .env

# 6. Make wrapper script executable
if [ -f "run_server.sh" ]; then
    echo "Making run_server.sh executable..."
    chmod +x run_server.sh
else
    echo "Warning: run_server.sh not found. Skipping chmod."
fi

# 7. Print final instructions and configuration path

echo "---------------------------------------------------"
echo "Setup mostly complete!"
echo ""
echo "The final step is to configure your MCP host (e.g., Claude Desktop)."
echo "Run the following command inside the '$PROJECT_DIR' directory (with the venv active or using the venv python):"
echo "  python print_config_paths.py"
echo ""
echo "Then, copy the 'Wrapper Script Path ('command')' output and paste it into your"
echo "MCP host's configuration file (e.g., claude_desktop_config.json)."
echo "The 'args' field in the config should be an empty list: []."
echo ""
echo "Example host config snippet:"
python print_config_paths.py # Run the helper script to show the path
echo ""
echo "Note for Windows Users: The run_server.sh wrapper is for Linux/macOS."
echo "You may need to adapt it or use the alternative configuration method mentioned in the README."
echo "---------------------------------------------------"

cd .. # Go back to the root directory # No longer needed
echo "Setup script finished." 