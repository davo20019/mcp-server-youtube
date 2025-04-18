import sys
import os

def main():
    """Prints the absolute path required for MCP host configuration using the wrapper script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    wrapper_script_path = os.path.abspath(os.path.join(script_dir, 'run_server.sh'))
    project_root = os.path.abspath(os.path.join(script_dir))

    # Basic check if the wrapper script exists
    if not os.path.exists(wrapper_script_path):
        print(f"Error: Wrapper script not found at {wrapper_script_path}", file=sys.stderr)
        print(f"Please ensure 'run_server.sh' exists in the directory: {script_dir}", file=sys.stderr)
        sys.exit(1)

    # Basic check if venv seems to exist (doesn't guarantee it's correctly set up)
    venv_path = os.path.join(project_root, '.venv')
    if not os.path.isdir(venv_path):
        print(f"Warning: Virtual environment directory not found at {venv_path}", file=sys.stderr)
        print("Please ensure you have created the virtual environment using 'uv venv' before running the server.", file=sys.stderr)

    # --- Start Refactored Output ---
    print("\n--- MCP Host Configuration ---")
    print("To connect this tool to your MCP host (e.g., Claude Desktop),")
    print("you need to configure the 'youtube' tool entry.")

    print("\n1. Set the 'command' field to this wrapper script path:")
    print(f'   "{wrapper_script_path}"')
    print("   (The 'args' field should usually be an empty list: [])")


    print("\n2. Example full MCP JSON configuration (copy/update your mcp.json):")
    print(f'''
{{
  "mcpServers": {{
      "youtube": {{
        "command": "{wrapper_script_path}",
        "args": [] 
      }},
      // Add other MCP server configurations here (like blender, etc.)
  }}
}}
    ''')

    print("\n--- Notes ---")
    print(" - If you need this configuration info again, re-run this script:")
    print(f"     ./.venv/bin/python {os.path.basename(__file__)}")
    print(" - Windows Users: The run_server.sh script is for Linux/macOS. See README for alternatives.")
    # --- End Refactored Output ---

if __name__ == "__main__":
    main() 