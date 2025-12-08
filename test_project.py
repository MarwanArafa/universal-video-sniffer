import pytest
from project import ask_format
from url_utils import is_valid_url, is_video_stream_url
from webpage_scanner import clean_filename
from unittest.mock import patch

# --- TEST 1: URL Validation (The 5 Platforms) ---
def test_is_valid_url():
    # 1. Twitter / X
    assert is_valid_url("https://x.com/ElonMusk/status/123456789") == True
    # 2. YouTube
    assert is_valid_url("https://www.youtube.com/watch?v=dQw4w9WgXcQ") == True
    # 3. TikTok
    assert is_valid_url("https://www.tiktok.com/@user/video/7891011") == True

    # Negative Test
    assert is_valid_url("ftp://not-supported.com") == False

# --- TEST 2: Filename Cleaning ---
def test_clean_filename():
    """
    Tests if the filename cleaner handles messy titles from these platforms.
    """
    # Case A: YouTube title with pipes and slashes
    dirty_yt = "Rick Astley - Never Gonna Give You Up (Official Video) | 4K / HD"
    assert clean_filename(dirty_yt) == "Rick Astley - Never Gonna Give You Up (Official Video)  4K  HD"

    # Case B: Twitter status with emojis (should stay) but slashes gone
    dirty_tw = "Look at this! 🚀/👀"
    assert clean_filename(dirty_tw) == "Look at this! 🚀👀"

    # Case C: Long title truncation
    long_title = "A" * 150
    cleaned = clean_filename(long_title)
    assert len(cleaned) <= 100

# --- TEST 3: User Input Logic (Mocking) ---
def test_ask_format_input(monkeypatch):
    """
    Simulates a user typing '1' or '2' to ensure the menu works.
    """
    # Simulate typing '1'
    monkeypatch.setattr('builtins.input', lambda _: '1')
    assert ask_format() == 'mp4'

    # Simulate typing '2'
    monkeypatch.setattr('builtins.input', lambda _: '2')
    assert ask_format() == 'mp3'

# --- TEST 4: Stream Extension Logic ---
def test_is_video_stream_url():
    # Direct files
    assert is_video_stream_url("http://site.com/video.mp4") == True
    # HLS Streams
    assert is_video_stream_url("https://cdn.site.com/master.m3u8") == True
    assert is_video_stream_url("https://cdn.site.com/segment01.ts") == True
    # Not video
    assert is_video_stream_url("https://site.com/index.html") == False
