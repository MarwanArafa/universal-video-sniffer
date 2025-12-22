# 🎥 Universal Video Sniffer & Downloader

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![License](https://img.shields.io/badge/License-MIT-green.svg)
![CS50P](https://img.shields.io/badge/CS50P-Final_Project-yellow.svg)

> **⚠️ Legal Disclaimer:** This tool is for **educational purposes only**. Use only on content you own or have permission to download. You are responsible for any consequences, including account bans or legal actions.

## 📌 Overview

Universal Video Sniffer & Downloader is a Python-based tool that can detect and download video streams from various platforms using browser automation and smart stream detection. It was developed as a **final project for Harvard's CS50P** (CS50's Introduction to Programming with Python).

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
- Git (for cloning the repository)

### 📖 How to Use
1.  Run `python project.py`
2.  Paste the URL.
3.  **Important:** If the browser opens, **do not close it**. Click "Accept Cookies" or "Play" to help the sniffer find the video.
