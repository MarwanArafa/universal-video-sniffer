# 🎥 Universal Video Sniffer & Downloader

#### Video Demo:  <INSERT_YOUR_YOUTUBE_LINK_HERE>
#### Description:
A powerful, Python-based video downloader engine capable of detecting and downloading streams from complex websites (YouTube, Twitter/X, Pornhub, TopCinema, etc.). Unlike standard downloaders that rely on static HTML parsing, this project uses a **Network Sniffing Engine** (Selenium) to intercept browser traffic, capture authentication cookies, and detect encrypted HLS streams (`.m3u8`).

### 🚀 Features
* **Network Sniffer Engine:** Detects video links that are hidden by JavaScript.
* **Smart Anti-Bot Bypass:** Automatically runs a visible browser to pass human verification.
* **Stream Stitching:** Automatically detects `.m3u8` playlists and stitches chunks with FFmpeg.
* **Cookie Hijacking:** Steals session cookies to authenticate requests and bypass 403 errors.

### 🛠️ Installation
1.  **System Requirements:** Google Chrome & FFmpeg.
2.  **Python Dependencies:** `pip install -r requirements.txt`

### 📖 How to Use
1.  Run `python project.py`
2.  Paste the URL.
3.  **Important:** If the browser opens, **do not close it**. Click "Accept Cookies" or "Play" to help the sniffer find the video.
