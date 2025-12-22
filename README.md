# 🎥 Universal Video Sniffer & Downloader

**CS50P Final Project**  
*Marwan Arafa* · December 2025  

[Demo Video (to be added after recording – under 3 minutes)](https://youtube.com/link-to-your-video)  

> A powerful CLI tool that downloads **any video** just by pasting its link — from YouTube, Twitter/X, Instagram, Reddit, Vimeo, Dailymotion, or **any website** with an embedded video.  
> Future enhancement: If a page has multiple videos, the app will prompt you to select which one.

## 📖 Description

This project uses a **network sniffing engine** (Selenium) to detect hidden streams, capture cookies, and download videos that standard tools can't handle. It stitches HLS segments with FFmpeg and supports MP4 or MP3.

**Why it's universal:** No site-specific code—works on JavaScript-heavy or protected sites.

## 🚀 Features

- 🌐 Works on any video link (YouTube, Twitter/X, Instagram, Reddit, etc.)
- 🔍 Sniffs hidden `.m3u8` or direct streams
- 🛡️ Bypasses restrictions via real browser + cookies
- 🎞️ MP4 or MP3 output
- 📝 Auto-cleaned filenames from page title

## 🛠️ Installation

### System Requirements
- Google Chrome browser
- FFmpeg (for stitching and MP3 conversion)  
  Download: https://ffmpeg.org/download.html  

  Quick install commands:

![Installation Commands Screenshot](screenshot_install.png)  
*(Your screenshot showing FFmpeg install options and pip command)*

### Python Dependencies
```bash
pip install -r requirements.txt
