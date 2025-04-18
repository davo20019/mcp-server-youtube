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


@mcp.tool()
async def get_channel_details(channel_id: str) -> Dict[str, Any] | str:
    """Get detailed information for a specific YouTube channel.

    Args:
        channel_id: The ID of the YouTube channel.

    Returns:
        A dictionary containing channel details or an error message string.
    """
    youtube = get_youtube_service()
    if not youtube:
        return "Failed to initialize YouTube service. Check YOUTUBE_API_KEY environment variable."

    try:
        channel_response = youtube.channels().list(
            part="snippet,statistics",
            id=channel_id
        ).execute()

        if not channel_response.get("items"):
            return f"Channel with ID '{channel_id}' not found."

        item = channel_response["items"][0]
        details = {
            "title": item["snippet"]["title"],
            "description": item["snippet"].get("description", "N/A"), # Description might be empty
            "customUrl": item["snippet"].get("customUrl", "N/A"),
            "publishedAt": item["snippet"]["publishedAt"],
            "subscriberCount": item["statistics"].get("subscriberCount", "Hidden or N/A"), # May be hidden
            "videoCount": item["statistics"].get("videoCount", "N/A"),
            "viewCount": item["statistics"].get("viewCount", "N/A"),
        }
        return details

    except HttpError as e:
        if e.resp.status == 400:
            return f"An HTTP error {e.resp.status} occurred: {e.content}. This might indicate an invalid or missing API key (YOUTUBE_API_KEY) or an invalid channel ID format."
        return f"An HTTP error {e.resp.status} occurred: {e.content}"
    except Exception as e:
        return f"An unexpected error occurred getting channel details: {e}"


@mcp.tool()
async def list_channel_videos(channel_id: str, max_results: int = 10) -> Dict[str, Any] | str:
    """List recent videos uploaded by a specific YouTube channel.

    Args:
        channel_id: The ID of the YouTube channel.
        max_results: Maximum number of videos to return (default: 10).

    Returns:
        A dictionary containing a list of videos or an error message string.
    """
    youtube = get_youtube_service()
    if not youtube:
        return "Failed to initialize YouTube service. Check YOUTUBE_API_KEY environment variable."

    try:
        # Use search.list to find videos for a specific channel, ordered by date
        search_response = youtube.search().list(
            part="id,snippet",
            channelId=channel_id,
            maxResults=max_results,
            order="date",  # Get the most recent videos
            type="video"
        ).execute()

        results = []
        for search_result in search_response.get("items", []):
            # Ensure it's a video result (though type='video' should handle this)
            if search_result["id"].get("kind") == "youtube#video":
                results.append({
                    "title": search_result["snippet"]["title"],
                    "videoId": search_result["id"]["videoId"],
                    "publishedAt": search_result["snippet"]["publishedAt"],
                    "description": search_result["snippet"].get("description", "N/A"),
                })

        return {"videos": results}

    except HttpError as e:
        if e.resp.status == 400:
            return f"An HTTP error {e.resp.status} occurred: {e.content}. This might indicate an invalid or missing API key (YOUTUBE_API_KEY) or an invalid channel ID."
        # Handle specific errors like channel not found (often a 404, but check API docs)
        # For now, general HTTP error handling
        return f"An HTTP error {e.resp.status} occurred: {e.content}"
    except Exception as e:
        return f"An unexpected error occurred listing channel videos: {e}"


@mcp.tool()
async def search_playlists(query: str, max_results: int = 5) -> Dict[str, Any] | str:
    """Search YouTube for playlists based on a query.

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
            type="playlist"  # Search specifically for playlists
        ).execute()

        results = []
        for search_result in search_response.get("items", []):
            # Ensure it's a playlist result
            if search_result["id"].get("kind") == "youtube#playlist":
                results.append({
                    "title": search_result["snippet"]["title"],
                    "playlistId": search_result["id"]["playlistId"],
                    "channelTitle": search_result["snippet"]["channelTitle"],
                    "channelId": search_result["snippet"]["channelId"],
                    "description": search_result["snippet"].get("description", "N/A"),
                    "publishedAt": search_result["snippet"]["publishedAt"],
                })

        return {"playlists": results}

    except HttpError as e:
        if e.resp.status == 400:
            return f"An HTTP error {e.resp.status} occurred: {e.content}. This might indicate an invalid or missing API key (YOUTUBE_API_KEY)."
        return f"An HTTP error {e.resp.status} occurred: {e.content}"
    except Exception as e:
        return f"An unexpected error occurred during playlist search: {e}"


@mcp.tool()
async def get_playlist_items(playlist_id: str, max_results: int = 10) -> Dict[str, Any] | str:
    """List the videos contained within a specific YouTube playlist.

    Args:
        playlist_id: The ID of the YouTube playlist.
        max_results: Maximum number of playlist items to return (default: 10).

    Returns:
        A dictionary containing a list of playlist items (videos) or an error message string.
    """
    youtube = get_youtube_service()
    if not youtube:
        return "Failed to initialize YouTube service. Check YOUTUBE_API_KEY environment variable."

    try:
        playlist_items_response = youtube.playlistItems().list(
            part="snippet,contentDetails",  # contentDetails contains videoId
            playlistId=playlist_id,
            maxResults=max_results
        ).execute()

        results = []
        for item in playlist_items_response.get("items", []):
            snippet = item.get("snippet", {})
            content_details = item.get("contentDetails", {})
            video_id = content_details.get("videoId")

            # Only include items that have a video ID
            if video_id:
                results.append({
                    "title": snippet.get("title", "N/A"),
                    "videoId": video_id,
                    "position": snippet.get("position", -1),
                    "publishedAt": snippet.get("publishedAt", "N/A"), # When video was added to playlist
                    "videoPublishedAt": content_details.get("videoPublishedAt", "N/A"), # When video was originally published
                    "description": snippet.get("description", "N/A"),
                    "channelTitle": snippet.get("videoOwnerChannelTitle", "N/A"),
                    "channelId": snippet.get("videoOwnerChannelId", "N/A"),
                })

        return {"playlistItems": results}

    except HttpError as e:
        if e.resp.status == 400:
            return f"An HTTP error {e.resp.status} occurred: {e.content}. This might indicate an invalid or missing API key (YOUTUBE_API_KEY) or an invalid playlist ID."
        if e.resp.status == 404: # Playlist not found is typically 404
             return f"Playlist with ID '{playlist_id}' not found or private."
        return f"An HTTP error {e.resp.status} occurred: {e.content}"
    except Exception as e:
        return f"An unexpected error occurred getting playlist items: {e}"


@mcp.tool()
async def get_related_videos(video_id: str, max_results: int = 5) -> Dict[str, Any] | str:
    """Find videos related to a specific YouTube video.

    Args:
        video_id: The ID of the YouTube video to find related videos for.
        max_results: Maximum number of related videos to return (default: 5).

    Returns:
        A dictionary containing a list of related videos or an error message string.
    """
    youtube = get_youtube_service()
    if not youtube:
        return "Failed to initialize YouTube service. Check YOUTUBE_API_KEY environment variable."

    try:
        # Use search.list with relatedToVideoId
        search_response = youtube.search().list(
            part="id,snippet",
            relatedToVideoId=video_id,
            maxResults=max_results,
            type="video"  # Ensure we only get videos
        ).execute()

        results = []
        for search_result in search_response.get("items", []):
            # Double check kind just in case
            if search_result["id"].get("kind") == "youtube#video":
                results.append({
                    "title": search_result["snippet"]["title"],
                    "videoId": search_result["id"]["videoId"],
                    "channelTitle": search_result["snippet"]["channelTitle"],
                    "channelId": search_result["snippet"]["channelId"],
                    "description": search_result["snippet"].get("description", "N/A"),
                    "publishedAt": search_result["snippet"]["publishedAt"],
                })

        # It's possible the API returns no related videos even if the original video exists
        return {"relatedVideos": results}

    except HttpError as e:
        if e.resp.status == 400:
             # Could be bad API key or invalid videoId format
            return f"An HTTP error {e.resp.status} occurred: {e.content}. This might indicate an invalid or missing API key (YOUTUBE_API_KEY) or invalid video ID format."
        if e.resp.status == 404:
            # The video specified by relatedToVideoId might not exist
             return f"Video with ID '{video_id}' not found, cannot find related videos."
        return f"An HTTP error {e.resp.status} occurred: {e.content}"
    except Exception as e:
        return f"An unexpected error occurred getting related videos: {e}"


@mcp.tool()
async def get_popular_videos(
    region_code: str = 'US',
    video_category_id: str = '0',
    max_results: int = 10
) -> Dict[str, Any] | str:
    """List the most popular videos currently trending in a specific region or category.

    Args:
        region_code: ISO 3166-1 alpha-2 country code (e.g., 'US', 'GB', 'JP'). Default is 'US'.
        video_category_id: The category ID. '0' typically represents all categories. Default is '0'.
                           (See YouTube API docs for specific category IDs if needed).
        max_results: Maximum number of popular videos to return (default: 10).

    Returns:
        A dictionary containing a list of popular videos or an error message string.
    """
    youtube = get_youtube_service()
    if not youtube:
        return "Failed to initialize YouTube service. Check YOUTUBE_API_KEY environment variable."

    try:
        popular_videos_response = youtube.videos().list(
            part="id,snippet,statistics,contentDetails", # Include more details for popular videos
            chart='mostPopular',
            regionCode=region_code,
            videoCategoryId=video_category_id,
            maxResults=max_results
        ).execute()

        results = []
        for item in popular_videos_response.get("items", []):
            snippet = item.get("snippet", {})
            stats = item.get("statistics", {})
            content = item.get("contentDetails", {})
            results.append({
                "title": snippet.get("title", "N/A"),
                "videoId": item.get("id", "N/A"),
                "channelTitle": snippet.get("channelTitle", "N/A"),
                "channelId": snippet.get("channelId", "N/A"),
                "categoryId": snippet.get("categoryId", "N/A"),
                "publishedAt": snippet.get("publishedAt", "N/A"),
                "viewCount": stats.get("viewCount", "N/A"),
                "likeCount": stats.get("likeCount", "N/A"),
                "commentCount": stats.get("commentCount", "N/A"),
                "duration": content.get("duration", "N/A"),
                "description": snippet.get("description", "N/A"), # Might be useful context
            })

        return {"popularVideos": results}

    except HttpError as e:
        if e.resp.status == 400:
             # Could be bad API key, invalid regionCode or categoryId
            return f"An HTTP error {e.resp.status} occurred: {e.content}. Check API key, region code ('{region_code}'), or category ID ('{video_category_id}')."
        return f"An HTTP error {e.resp.status} occurred: {e.content}"
    except Exception as e:
        return f"An unexpected error occurred getting popular videos: {e}"


# --- Running the Server ---
if __name__ == "__main__":
    print("Starting YouTube MCP Server (reading API Key from environment)...")
    # Re-add the warning about missing environment variable API_KEY
    if not API_KEY:
        print("Warning: YOUTUBE_API_KEY is not set. Tools will likely fail.")
    # Initialize and run the server via stdio
    mcp.run(transport='stdio')
