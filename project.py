import sys
import os
from webpage_scanner import extract_media_data
from video_downloader import download_with_engine


def is_valid_url(url):
    # Checks if the URL starts with http or https
    return url.startswith("http://") or url.startswith("https://")

def get_extension(choice):
    # Returns the file extension based on user input
    if choice == "1":
        return "mp4"
    elif choice == "2":
        return "mp3"
    else:
        return None

def create_filename(title, extension):
    # Removes special characters to create a safe filename
    safe_title = "".join(c for c in title if c.isalnum() or c in (' ', '-', '_')).strip()
    return f"{safe_title}.{extension}"

def print_banner():
    # Prints the welcome screen and instructions
    print("\n" + "="*60)
    print("      🎥  UNIVERSAL VIDEO SNIFFER & DOWNLOADER  🎥")
    print("="*60)
    print("⚠️  LEGAL WARNING: EDUCATIONAL PURPOSE ONLY")
    print("   - Do not use this tool for piracy.")
    print("-" * 60)
    print("📖  HOW TO USE:")
    print("   1. Paste the URL below.")
    print("   2. If a Browser Window opens: DO NOT CLOSE IT!")
    print("   3. INTERACT with the site (Click Play, Close Ads).")
    print("="*60 + "\n")


def main():
    # Ensure downloads directory exists
    if not os.path.exists("downloads"):
        os.makedirs("downloads")

    print_banner()
    
    # Get URL from user
    try:
        user_url = input("Enter video URL: ").strip()
    except KeyboardInterrupt:
        sys.exit(0)

    # Check if URL is valid using helper function
    if not is_valid_url(user_url):
        print("❌ Error: That doesn't look like a valid URL.")
        sys.exit(1)

    # Get format choice
    user_format = None
    while user_format is None:
        print("Download as:")
        print("  [1] MP4 (Video + Audio)")
        print("  [2] MP3 (Audio only)")
        choice = input("Choose (1 or 2): ").strip()
        
        # Use helper function to get extension
        user_format = get_extension(choice)
        
        if user_format is None:
            print("❌ Invalid choice. Please enter 1 or 2.")

    try:
        # Extract media info using the external scanner module
        video_url, cookies, user_agent, video_title = extract_media_data(user_url)
    except KeyboardInterrupt:
        print("\n\n❌ Process cancelled by user.")
        sys.exit(0)
    
    if video_url:
        print(f"   [Main] Stream found! Title: {video_title}")
        
        # Generate safe filename using helper function
        filename = create_filename(video_title, user_format)
        
        # Download the file
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
