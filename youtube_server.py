import os
from typing import Any, List, Dict
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Re-add loading .env file
load_dotenv()

# Initialize FastMCP server
mcp = FastMCP("youtube")

# --- Constants and Configuration ---
# Revert to reading API key from environment variable
API_KEY = os.getenv("YOUTUBE_API_KEY")
API_SERVICE_NAME = "youtube"
API_VERSION = "v3"

# Re-add the check for environment variable API_KEY
if not API_KEY:
    print("Error: YOUTUBE_API_KEY environment variable not set.")
    print("Please create a .env file in the project root with YOUTUBE_API_KEY=YOUR_API_KEY")
    # Or set it in your system environment

# --- Helper Function ---
# Revert to using the global API_KEY from environment
def get_youtube_service() -> Any | None:
    """Builds and returns the YouTube API service object using the environment API key."""
    if not API_KEY:
        print("Cannot build YouTube service: API key is missing from environment.")
        return None
    try:
        # Use the API_KEY read from environment
        service = build(API_SERVICE_NAME, API_VERSION, developerKey=API_KEY)
        return service
    except Exception as e:
        print(f"Error building YouTube service: {e}")
        return None

# --- Tool Implementations ---

@mcp.tool()
async def search_videos(query: str, max_results: int = 5) -> Dict[str, Any] | str:
    """Search YouTube for videos based on a query.

    Args:
        query: The search term.
        max_results: Maximum number of results to return (default: 5).

    Returns:
        A dictionary containing search results or an error message string.
    """
    youtube = get_youtube_service()
    if not youtube:
        return "Failed to initialize YouTube service. Check YOUTUBE_API_KEY environment variable."

    try:
        search_response = youtube.search().list(
            q=query,
            part="id,snippet",
            maxResults=max_results,
            type="video"  # Only search for videos
        ).execute()

        results = []
        for search_result in search_response.get("items", []):
            results.append({
                "title": search_result["snippet"]["title"],
                "videoId": search_result["id"]["videoId"],
                "channelTitle": search_result["snippet"]["channelTitle"],
                "description": search_result["snippet"]["description"],
            })

        return {"videos": results}

    except HttpError as e:
        # Check if the error is due to an invalid API key (often a 400 error)
        if e.resp.status == 400:
            return f"An HTTP error {e.resp.status} occurred: {e.content}. This might indicate an invalid or missing API key (YOUTUBE_API_KEY)."
        return f"An HTTP error {e.resp.status} occurred: {e.content}"
    except Exception as e:
        return f"An unexpected error occurred during search: {e}"


@mcp.tool()
async def get_video_details(video_id: str) -> Dict[str, Any] | str:
    """Get detailed information for a specific YouTube video.

    Args:
        video_id: The ID of the YouTube video.

    Returns:
        A dictionary containing video details or an error message string.
    """
    youtube = get_youtube_service()
    if not youtube:
        return "Failed to initialize YouTube service. Check YOUTUBE_API_KEY environment variable."

    try:
        video_response = youtube.videos().list(
            part="snippet,contentDetails,statistics",
            id=video_id
        ).execute()

        if not video_response.get("items"):
            return f"Video with ID '{video_id}' not found."

        item = video_response["items"][0]
        details = {
            "title": item["snippet"]["title"],
            "description": item["snippet"]["description"],
            "channelTitle": item["snippet"]["channelTitle"],
            "publishedAt": item["snippet"]["publishedAt"],
            "duration": item["contentDetails"].get("duration", "N/A"),
            "viewCount": item["statistics"].get("viewCount", "N/A"),
            "likeCount": item["statistics"].get("likeCount", "N/A"),
            "commentCount": item["statistics"].get("commentCount", "N/A"),
        }
        return details

    except HttpError as e:
        # Check if the error is due to an invalid API key (often a 400 error)
        if e.resp.status == 400:
            return f"An HTTP error {e.resp.status} occurred: {e.content}. This might indicate an invalid or missing API key (YOUTUBE_API_KEY)."
        return f"An HTTP error {e.resp.status} occurred: {e.content}"
    except Exception as e:
        return f"An unexpected error occurred getting details: {e}"


# --- Running the Server ---
if __name__ == "__main__":
    print("Starting YouTube MCP Server (reading API Key from environment)...")
    # Re-add the warning about missing environment variable API_KEY
    if not API_KEY:
        print("Warning: YOUTUBE_API_KEY is not set. Tools will likely fail.")
    # Initialize and run the server via stdio
    mcp.run(transport='stdio')
