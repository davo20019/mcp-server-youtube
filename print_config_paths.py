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

    print("Configuration for MCP host (e.g., Claude Desktop):")
    print("Use the following absolute path for the 'command' field.")
    print("The 'args' field should typically be empty when using this wrapper script.")
    print("\nWrapper Script Path ('command'):")
    print(f'"{wrapper_script_path}"')

    print("\nExample JSON snippet:")
    print(f'''
    "youtube": {{
        "command": "{wrapper_script_path}",
        "args": [] // Usually empty when using the wrapper
    }}
    ''')
    print("\nNote: Ensure the wrapper script ('run_server.sh') has execute permissions (chmod +x run_server.sh).")
    print("Also ensure you have run 'uv venv' and 'uv sync' to set up the environment.")

if __name__ == "__main__":
    main() 