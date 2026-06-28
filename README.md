# 🎥 Universal Video Sniffer & Downloader

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![CS50P](https://img.shields.io/badge/CS50P-Final_Project-yellow.svg)

> ⚠️ **Legal Notice:** This tool is for **educational purposes only**. Only download content you own or have permission to download. You are fully responsible for how you use it.

---

## 📺 Video Demo
**[Watch the Demo Here](https://github.com/MarwanArafa/universal-video-sniffer)** *(coming soon)*

---

## 📌 What does it do?

You paste a video URL. It downloads the video to your computer as MP4 or MP3. That's it.

It works by scanning the page for the actual video stream — the same stream your browser plays — and downloads it directly.

---

## 💻 Supported Platforms

| Site | Status |
|---|---|
| Most video platforms | ✅ Fast direct extraction (flashvars-based) |
| YouTube | 🔄 Browser scan fallback |
| Twitter / X | 🔄 Browser scan fallback |
| TikTok | 🔄 Browser scan fallback |
| Vimeo | 🔄 Browser scan fallback |
| Most other sites | 🔄 Browser scan fallback |

---

## 🛠️ Installation (do this once)

### Step 1 — Make sure you have Python
Open a terminal and run:
```
python --version
```
You need Python 3.8 or higher. If you don't have it, download it from [python.org](https://python.org).

### Step 2 — Install FFmpeg
FFmpeg is a free tool that handles video/audio processing. You need it.

- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html), extract it, and add the `bin` folder to your PATH.
- **Mac:** Run `brew install ffmpeg` in Terminal (requires [Homebrew](https://brew.sh)).
- **Linux:** Run `sudo apt install ffmpeg` or `sudo pacman -S ffmpeg`.

To verify it works, run: `ffmpeg -version`

### Step 3 — Install Google Chrome
Make sure Google Chrome is installed on your system. The tool uses it for sites that need a browser to find the video.

### Step 4 — Install Python dependencies
In the project folder, run:
```
pip install -r requirements.txt
```

---

## ▶️ How to Use

Run this in the project folder:
```
python project.py
```

Then:
1. Paste the video URL when asked
2. Choose MP4 (video) or MP3 (audio only)
3. Wait — a progress bar will show the download
4. Find your file in the `downloads/` folder

---

## 📁 Project Structure

| File | What it does |
|---|---|
| `project.py` | Main entry point — handles user input and flow |
| `webpage_scanner.py` | Finds the video stream URL from a page |
| `video_downloader.py` | Downloads the stream using FFmpeg or direct HTTP |
| `url_utils.py` | URL validation helpers |
| `test_project.py` | Automated tests (run with `pytest`) |
| `requirements.txt` | Python dependencies |

---

## ❓ Troubleshooting

**"FFmpeg not installed"** → Go back to Step 2 above.

**"Could not detect any video stream"** → The site may use heavy anti-bot protection. Try a different URL or a different video.

**Download stops or is slow** → Normal for large videos. The progress bar shows time remaining.

**File saved but won't play** → Make sure you chose MP4. Some sites only provide HLS streams which need FFmpeg to assemble — this is handled automatically.

---

## 🔮 Planned Features
- Quality selector (1080p / 720p / 480p)
- Playlist/batch download
- Built-in site extractors for YouTube, Twitter, TikTok
- GUI version

---

## 👤 Author
**Marwan Arafa** — [GitHub](https://github.com/MarwanArafa) | [Portfolio](https://marwan-dev.me)

*Final project for Harvard's CS50P — Introduction to Programming with Python*
