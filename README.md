# MCP YouTube Server

This is a simple Model Context Protocol (MCP) server that provides tools to interact with YouTube. It allows an MCP host application (like Claude for Desktop) to:

*   Search for YouTube videos.
*   Get detailed information about specific YouTube videos.

## Requirements

*   Python 3.10 or higher.
*   [uv](https://github.com/astral-sh/uv) (recommended for environment management) or `pip`.
*   A YouTube Data API v3 Key. You can obtain one from the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).

## Installation

1.  **Clone the repository** (or download the source code):
    ```bash
    git clone https://github.com/davo20019/mcp-server-youtube.git
    cd mcp-server-youtube
    ```

2.  **Create and activate a virtual environment** (using `uv`):
    ```bash
    uv venv
    source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
    ```
    Alternatively, using standard `venv`:
    ```bash
    python -m venv .venv
    source .venv/bin/activate # On Windows use `.venv\Scripts\activate`
    ```

3.  **Install dependencies** (using `uv`):
    ```bash
    uv pip install -r requirements.txt
    ```
    Alternatively, using `pip`:
    ```bash
    pip install -r requirements.txt
    ```

## Configuration

1.  **API Key:** This server requires a YouTube Data API v3 key.
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
    *   Create a project if you don't have one.
    *   Enable the "YouTube Data API v3".
    *   Create an API key credential.

2.  **`.env` File:** Create a file named `.env` in the root of the `mcp-server-youtube` project directory.
    *   Add your API key to this file like so:
        ```
        YOUTUBE_API_KEY=YOUR_ACTUAL_API_KEY_HERE
        ```
    *   Replace `YOUR_ACTUAL_API_KEY_HERE` with the key you obtained from Google Cloud.

## Running with an MCP Host (Example: Claude for Desktop)

To use this server with an MCP host application like Claude for Desktop, you need to configure the host to launch the server.

1.  **Find your Claude for Desktop config file:**
    *   macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
    *   Windows: `%APPDATA%\Claude\claude_desktop_config.json` (You might need to create the `Claude` folder and the file).

2.  **Edit the config file:** Add the following entry under the `mcpServers` key. **Make sure to replace the placeholder paths with the correct *absolute paths* on your system.**

    ```json
    {
        "mcpServers": {
            // ... other servers might be here ...

            "youtube": {
                "command": "/ABSOLUTE/PATH/TO/mcp-server-youtube/.venv/bin/python",
                "args": [
                    "/ABSOLUTE/PATH/TO/mcp-server-youtube/youtube_server.py"
                ]
            }
        }
    }
    ```
    *   **`command`:** The absolute path to the `python` executable *inside* the `.venv` directory you created during installation.
    *   **`args`:** The absolute path to the `youtube_server.py` script within the project directory.

3.  **Restart Claude for Desktop.**

## Usage

Once the server is configured in your MCP host and the host is restarted, the YouTube tools should become available.
You can then use natural language prompts within the host application:

*   "Search YouTube for 'python async tutorial'"
*   "Find videos about 'MCP server development'"
*   "Get the details for YouTube video ID XXXXXXX" (Replace XXXXXXX with a valid ID)

The host application will communicate with the local `youtube_server.py` process to fulfill these requests.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests if you have improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
