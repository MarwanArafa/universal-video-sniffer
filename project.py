import sys
import os
import time
from webpage_scanner import extract_media_data
from video_downloader import download_with_engine
from url_utils import is_valid_url

def print_banner():
    print("\n" + "="*60)
    print("      🎥  UNIVERSAL VIDEO SNIFFER & DOWNLOADER  🎥")
    print("="*60)
    print("⚠️  LEGAL WARNING: EDUCATIONAL PURPOSE ONLY")
    print("   - Do not use this tool for piracy.")
    print("   - You are responsible for any account bans.")
    print("-" * 60)
    print("📖  HOW TO USE:")
    print("   1. Paste the URL below.")
    print("   2. If a Browser Window opens: DO NOT CLOSE IT!")
    print("   3. INTERACT with the site (Click Play, Close Ads).")
    print("   4. Wait for the script to detect the video stream.")
    print("="*60 + "\n")

def ask_format():
    while True:
        print("Download as:")
        print("  [1] MP4 (Video + Audio)")
        print("  [2] MP3 (Audio only)")
        choice = input("Choose (1 or 2): ").strip()
        if choice == "1": return "mp4"
        if choice == "2": return "mp3"

def main():
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    print_banner()
    
    try:
        user_url = input("Enter video URL: ").strip()
    except KeyboardInterrupt:
        sys.exit(0)

    if not is_valid_url(user_url):
        print("❌ Error: That doesn't look like a valid URL.")
        sys.exit(1)

    user_format = ask_format()

    try:
        # UNPACK 4 VALUES NOW (Added video_title)
        video_url, cookies, user_agent, video_title = extract_media_data(user_url)
    except KeyboardInterrupt:
        print("\n\n❌ Process cancelled by user.")
        sys.exit(0)
    
    if video_url:
        print(f"   [Main] Stream found! Title: {video_title}")
        
        # USE THE REAL TITLE FOR THE FILENAME
        filename = f"{video_title}.{user_format}"
        
        success = download_with_engine(video_url, cookies, user_agent, filename, user_format)
        
        if success:
            print(f"\n✅ Success! Saved as: 'downloads/{filename}'")
        else:
            print("\n❌ Download failed.")
    else:
        print("\n❌ Could not detect any video stream.")
        print("   (Did you remember to press 'Play' in the browser window?)")

if __name__ == "__main__":
    main()