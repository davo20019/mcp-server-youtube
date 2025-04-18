# MCP YouTube Server

This is a simple Model Context Protocol (MCP) server that provides tools to interact with YouTube. It allows an MCP host application (like Claude for Desktop) to:

*   Search for YouTube videos.
*   Get detailed information about specific YouTube videos.

## Requirements

*   Python 3.10 or higher.
*   [uv](https://github.com/astral-sh/uv) (must be installed before running setup).
*   A YouTube Data API v3 Key. You can obtain one from the [Google Cloud Console](https://console.cloud.google.com/apis/credentials).
*   `bash` compatible shell (for running the setup script, primarily Linux/macOS).

## Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/davo00019/mcp-server-youtube.git
    cd mcp-server-youtube
    ```

2.  **Run the setup script:**
    *   Ensure you have `uv` installed (`pip install uv` or see [uv installation](https://github.com/astral-sh/uv)).
    *   From **within** the `mcp-server-youtube` directory, run:
        ```bash
        bash setup.sh
        ```
    *   The script will:
        *   Check for `uv`.
        *   Create a virtual environment (`.venv`) inside `mcp-server-youtube`.
        *   Install dependencies (`uv sync`).
        *   Prompt you for your YouTube API Key and create the `.env` file.
        *   Make the server wrapper script executable.
        *   Print the final instructions and the path needed for your MCP host configuration.

3.  **Configure MCP Host:**
    *   Follow the instructions printed at the end of the `setup.sh` script.
    *   Copy the 'Wrapper Script Path' provided by the script.
    *   Paste this path into your MCP host's configuration file (e.g., `claude_desktop_config.json`) as the `command` for the `youtube` server, ensuring the `args` are `[]`.

## Configuration Details (`.env`)

The `setup.sh` script will prompt you for your YouTube Data API v3 key and create a `.env` file in the `mcp-server-youtube` directory with the following content:

```
YOUTUBE_API_KEY=YOUR_API_KEY_HERE
```

If you need to change the key later, you can edit this `.env` file directly.

## Running with an MCP Host (Example: Claude for Desktop)

After running the `setup.sh` script and configuring your MCP host as described above (Step 3 in Installation & Setup), the server should launch automatically when your host application starts.

1.  **Find your Claude for Desktop config file:**
    *   macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
    *   Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2.  **Edit the config file:** Update the `mcpServers` section. The `setup.sh` script (via `print_config_paths.py`) provides an example JSON structure showing exactly how to configure the `youtube` server entry, including the correct absolute path for the `command` field. Copy and paste or adapt the example from the script's output into your configuration file.

3.  **Restart Claude for Desktop.**

    *   **Windows Users Note:** The `setup.sh` and `run_server.sh` scripts are designed for `bash` environments (Linux/macOS). You might need to perform the setup steps manually (create venv, install deps, create `.env`, configure host with direct python/script paths) or adapt the scripts for Windows (e.g., create a `run_server.bat`).

## Usage

Once the server is configured in your MCP host and the host is restarted, the YouTube tools should become available.
You can then use natural language prompts within the host application:

*   "Search YouTube for 'python async tutorial'"
*   "Find videos about 'MCP server development'"
*   "Get the details for YouTube video ID XXXXXXX" (Replace XXXXXXX with a valid ID)

The host application will communicate with the local `youtube_server.py` process to fulfill these requests.

## Available Tools

The server currently provides the following tools:

*   `search_videos(query: str, max_results: int = 5)`: Searches YouTube for videos based on a query string.
*   `get_video_details(video_id: str)`: Fetches detailed information (snippet, statistics, content details) for a specific video ID.
*   `get_channel_details(channel_id: str)`: Fetches detailed information (snippet, statistics) for a specific channel ID.
*   `list_channel_videos(channel_id: str, max_results: int = 10)`: Lists recent videos uploaded by a specific channel ID.
*   `search_playlists(query: str, max_results: int = 5)`: Searches YouTube for playlists matching a query string.
*   `get_playlist_items(playlist_id: str, max_results: int = 10)`: Lists the videos contained within a specific playlist ID.
*   `get_related_videos(video_id: str, max_results: int = 5)`: Finds videos that YouTube deems related to a given video ID.
*   `get_popular_videos(region_code: str = 'US', video_category_id: str = '0', max_results: int = 10)`: Lists the most popular videos currently trending in a specific region or category.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests if you have improvements or bug fixes.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
