# Function that randomly selects a query to use for the background video
def get_random_query():
    import random
    queries = ["city", "nature", "ocean", "forest"]
    return random.choice(queries)

# Function that gets the background image for the video
def get_background_video(api_key, query="city"):
    import os, requests
    from datetime import datetime

    headers = {"Authorization": api_key}
    params = {
        "query": query,
        "orientation": "portrait",
        "per_page": 1,
        "size": "medium"
    }

    response = requests.get("https://api.pexels.com/videos/search", headers=headers, params=params)
    response.raise_for_status()
    data = response.json()

    if not data["videos"]:
        raise ValueError(f"No videos found for query: {query}")

    video_url = data["videos"][0]["video_files"][0]["link"]

    vid_response = requests.get(video_url, stream=True)
    vid_response.raise_for_status()
    return vid_response.content

# Function that retrieves stock media files from a specified directory
def get_stock_media_files(directory: str):
    from pathlib import Path
    import os

    # Get absolute path based on script's parent directory and the given directory
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(script_dir)
    stock_media_dir = os.path.join(parent_dir, directory)

    folder = Path(stock_media_dir)
    return [f.name for f in folder.glob('*.mp4') if f.is_file()]

# Function to get the path of a specific stock media file
def get_stock_media_path(filename: str):
    from pathlib import Path
    import os

    # Get the parent directory of the current script
    script_dir = os.path.dirname(__file__)
    parent_dir = os.path.dirname(script_dir)
    # Build the path to the file within 'stock_media'
    file_path = Path(parent_dir) / "stock_media" / filename
    return file_path