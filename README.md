# 🎥 Universal Video Sniffer & Downloader

#### Video Demo: [INSERT YOUR YOUTUBE LINK HERE]

## Description
This is a powerful, Python-based video downloader that grabs any type of video just by pasting the link—from YouTube, Twitter/X, Instagram, Reddit, or any website with embedded media.

Unlike standard downloaders that rely on static HTML parsing, this project uses a **Network Sniffing Engine (Selenium)** to intercept browser traffic, capture authentication cookies, and detect encrypted HLS streams (`.m3u8`). It handles MP4 or MP3 formats, stitches segmented videos automatically with FFmpeg, and focuses on educational purposes only.

This versatility allows it to work on complex sites like TopCinema, Vimeo, Dailymotion, and generic embeds.

> **Note:** The tool targets the main playable stream detected after user interaction (like clicking play). Future enhancements may include prompting the user to select from multiple detected videos.

The project is modular, includes unit tests, and emphasizes real-world problem-solving by bypassing anti-bot measures through manual browser interaction.

---

## 🚀 Features

* **Network Sniffer Engine:** Detects video links hidden by JavaScript, including HLS playlists (`.m3u8`) and direct MP4 streams.
* **Smart Anti-Bot Bypass:** Automatically launches a visible browser instance to pass human verification and capture session data.
* **Stream Stitching:** Automatically detects `.m3u8` playlists and stitches video segments together using FFmpeg for a seamless download.
* **Cookie Hijacking:** Steals session cookies from the browser to authenticate requests and bypass `403 Forbidden` errors.
* **Format Options:** Supports downloading as **MP4** (Video + Audio) or **MP3** (Audio only).
* **Title Detection:** Automatically detects the video title from the webpage and cleans it for use as the filename.
* **Universal Compatibility:** Tested on YouTube, Twitter/X, Instagram, Reddit, Vimeo, Dailymotion, and many other sites.

---

## 🛠️ Installation

### 1. System Requirements
* **Google Chrome:** Required for Selenium automation.
* **FFmpeg:** You must install FFmpeg and add it to your system PATH.
    * **macOS:** `brew install ffmpeg`
    * **Ubuntu/Linux:** `sudo apt install ffmpeg`
    * **Windows:** Download from [ffmpeg.org](https://ffmpeg.org) or use `choco install ffmpeg`.

### 2. Python Dependencies
Install the required packages using pip:

```bash
pip install -r requirements.txt
