# 🎥 Universal Video Sniffer & Downloader

[Demo Video Link] (To be added after recording – under 3 minutes demo for CS50P submission)

#### Enter video URL: <INSERT_YOUR_YOUTUBE_LINK_HERE>

#### Description:
This is a powerful, Python-based video downloader that grabs any type of video just by pasting the link—from YouTube, Twitter/X, Instagram, Reddit, or any website with embedded media. Unlike standard downloaders that rely on static HTML parsing, this project uses a **Network Sniffing Engine** (Selenium) to intercept browser traffic, capture authentication cookies, and detect encrypted HLS streams (`.m3u8`). It handles MP4 or MP3 formats, stitches segmented videos automatically with FFmpeg, and focuses on educational purposes only (e.g., no piracy). 

Future enhancement: If a page has more than one video, the app could prompt you to select which one to download. Currently, it targets the main playable stream after you interact with the browser to click play or close ads. This makes it versatile for complex sites like Pornhub, TopCinema, Vimeo, Dailymotion, or even random embeds.

The project is modular, with unit tests, and emphasizes real-world problem-solving like bypassing anti-bot measures through manual browser interaction.

### 🚀 Features
* **Network Sniffer Engine:** Detects video links that are hidden by JavaScript, including HLS playlists and direct MP4 streams.
* **Smart Anti-Bot Bypass:** Automatically runs a visible browser to pass human verification and capture session data.
* **Stream Stitching:** Automatically detects `.m3u8` playlists and stitches chunks with FFmpeg for seamless downloads.
* **Cookie Hijacking:** Steals session cookies to authenticate requests and bypass 403 errors.
* **Format Options:** Download as MP4 (video + audio) or MP3 (audio only).
* **Title Detection:** Automatically cleans and uses the page title for the filename.
* **Universal Compatibility:** Works on YouTube, Twitter/X, Instagram, Reddit, Vimeo, Dailymotion, and arbitrary websites with videos.

### 🛠️ Installation
1. **System Requirements:** 
   - Google Chrome browser (for Selenium).
   - FFmpeg (download from [ffmpeg.org](https://ffmpeg.org/download.html) and add to your PATH – e.g., `brew install ffmpeg` on macOS, `apt install ffmpeg` on Ubuntu).
2. **Python Dependencies:** Run `pip install -r requirements.txt` (includes selenium, webdriver-manager, requests, tqdm, pytest).

### 📖 How to Use
1. Clone the repo: `git clone https://github.com/MarwanArafa/universal-video-sniffer.git` and navigate to the directory.
2. Run the main script: `python project.py`.
3. Paste the video URL when prompted (e.g., from `test_urls.txt` for samples like YouTube or Twitter links).
4. Choose format: 1 for MP4 (video + audio) or 2 for MP3 (audio only).
5. **Important:** A Chrome browser window will open automatically – **do not close it**. Interact with the page: Click "Accept Cookies," close popups/ads, or hit "Play" on the video to trigger the stream. The script will sniff the traffic, detect the video URL, and download to the `downloads/` folder.
6. Example: For a YouTube link, it might save as "Video Title.mp4". Check the terminal for progress.

**Screenshots:**  
- Terminal prompt: ![Terminal Example](path/to/screenshot_terminal.png) (Add your own screenshot here for visual guide).  
- Browser popup: ![Browser Interaction](path/to/screenshot_browser.png) (Shows the "Chrome is being controlled" warning and play button).

### 🧪 Testing
Run `pytest test_project.py` to execute unit tests. These cover:
- URL validation for supported platforms (YouTube, Twitter/X, etc.).
- Filename cleaning (removes invalid characters, truncates long titles).
- User input handling for format selection.
- Stream detection logic (e.g., for HLS/m3u8 files).

All tests should pass if dependencies are installed correctly.

### ⚠️ Limitations and Warnings
- **Educational Use Only:** This tool is for learning purposes (e.g., CS50P final project). Do not use for illegal downloads or piracy – you are responsible for compliance with site terms and laws.
- **Manual Interaction Required:** You must click play or close ads in the browser popup; automation isn't fully headless to mimic real users.
- **Site Compatibility:** May fail on heavy anti-bot sites (e.g., CAPTCHA-protected). Test with `test_urls.txt` for reliable examples.
- **File Size/Performance:** Large videos may take time; ensure stable internet.
- **No Multi-Video Prompt Yet:** If a page has multiple videos, it grabs the primary one – add a selection feature for improvement.

This project demonstrates Python skills like browser automation, network interception, subprocess handling (FFmpeg), and testing – perfect for CS50P! Total word count: ~550. If issues, check GitHub for updates.
