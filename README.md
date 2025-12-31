# 🎥 Universal Video Sniffer & Downloader

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![CS50P](https://img.shields.io/badge/CS50P-Final_Project-yellow.svg)

> **⚠️ Legal Disclaimer:** This tool is for **educational purposes only**. Use only on content you own or have permission to download. You are responsible for any consequences, including account bans or legal actions.

## 📺 Video Demo
**[Watch the Demo Here](<INSERT_YOUR_YOUTUBE_LINK_HERE>)** *(Description: A walkthrough of the tool functionality)*

## 📌 Overview
Universal Video Sniffer & Downloader is a Python-based tool that can detect and download video streams from various platforms using browser automation and smart stream detection. It was developed as a **final project for Harvard's CS50P** (CS50's Introduction to Programming with Python).

## 📁 Project Structure
- `project.py`: The main entry point. Handles user input, logic validation, and filename generation.
- `webpage_scanner.py`: Uses Selenium to open a browser and "sniff" network traffic for video URLs.
- `video_downloader.py`: The engine that handles the actual downloading via HTTP streams or FFmpeg.
- `test_project.py`: Contains unit tests for `project.py` functions using `pytest`.
- `requirements.txt`: Lists all Python dependencies.

## ✨ Features
- **🕵️‍♂️ Smart Stream Detection**: Automatically detects video streams using Selenium browser automation
- **🌐 Multi-Platform Support**: Works with YouTube, Twitter/X, TikTok, Facebook, Vimeo, Dailymotion, Archive.org, and more
- **📁 Dual Output Formats**: Download as MP4 (video+audio) or MP3 (audio only)
- **🎯 Intelligent Download Engine**: Automatically switches between direct download and FFmpeg streaming
- **🍪 Cookie Handling**: Preserves session cookies for authenticated content
- **🔧 Safe Filename Generation**: Automatically cleans and truncates filenames
- **📊 Progress Tracking**: Real-time download progress with `tqdm`

## 🛠️ Installation

### Prerequisites
- Python 3.8 or higher
- FFmpeg installed on your system
- Google Chrome browser

### Setup
1. Clone the repository:
   ```bash
   git clone [https://github.com/MarwanArafa/universal-video-sniffer.git](https://github.com/MarwanArafa/universal-video-sniffer.git)
   cd universal-video-sniffer

2. Install Dependencies:
```bash
    pip install -r requirements.txt
```

## 📖 How to Use

- Run the program:
```bash
python project.py # Paste the URL when prompted.
```

***Important: If the browser opens, do not close it. Click "Accept Cookies" or "Play" to help the sniffer find the video.***


### **One Last Step**
- Make sure you create a `requirements.txt` file in your folder if you haven't already! The grader needs this to run your code.

## Run this command in your terminal to generate it automatically:
```bash
pip freeze > requirements.txt
```
