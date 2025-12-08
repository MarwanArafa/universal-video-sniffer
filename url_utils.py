from urllib.parse import urlparse

# Extensions we consider valid for video files
VIDEO_EXTENSIONS = (
    '.mp4', '.webm', '.mkv', '.mov', '.avi', '.m4a', '.mp3',
    '.m3u8', '.ts', '.flv', '.wmv'
)

def is_valid_url(url: str) -> bool:
    """Returns True if the string looks like a valid HTTP URL."""
    if not isinstance(url, str):
        return False
    return url.startswith(("http://", "https://"))

def is_video_stream_url(url: str) -> bool:
    """Checks if a URL ends with a known video extension."""
    if not is_valid_url(url):
        return False
    return any(url.lower().endswith(ext) for ext in VIDEO_EXTENSIONS)