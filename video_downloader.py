import requests
import subprocess
import os
from tqdm import tqdm

def is_hls_playlist(url: str, cookies: dict, user_agent: str) -> bool:
    """
    Checks if the URL points to a Playlist (text file) instead of a Video file.
    It checks the URL extension and the Content-Type header.
    """
    # 1. Quick String Check
    if any(x in url for x in [".m3u8", "master.json", "manifest"]):
        return True
        
    # 2. The "ID Card" Check (Content-Type)
    try:
        session = requests.Session()
        session.cookies.update(cookies)
        # Fetch only headers (stream=True) to check file type
        response = session.get(url, headers={"User-Agent": user_agent}, stream=True, timeout=5)
        content_type = response.headers.get("Content-Type", "").lower()
        response.close()
        
        # If server says "mpegurl", it is a playlist
        if "mpegurl" in content_type or "x-mpegurl" in content_type:
            return True
    except:
        pass
    return False

def run_ffmpeg(url, cookies, user_agent, save_path, format_type):
    """
    Helper function to run FFmpeg.
    Handles both Video Stitching (copy) and Audio Extraction (mp3).
    """
    print("   [FFmpeg] Starting Stream Download...")
    
    # Format cookies into a string for FFmpeg
    cookie_str = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    
    cmd = [
        'ffmpeg', '-y',                 # Overwrite output without asking
        '-user_agent', user_agent,      # Pretend to be Chrome
        '-headers', f"Cookie: {cookie_str}", # Pass stolen cookies
        '-i', url                       # Input URL
    ]

    if format_type == "mp3":
        # Audio Only: Ignore video (-vn) and encode to MP3
        cmd.extend(['-vn', '-acodec', 'libmp3lame', '-q:a', '2']) 
    else:
        # Video: Copy the stream directly (no re-encoding = fast)
        cmd.extend(['-c', 'copy', '-bsf:a', 'aac_adtstoasc'])

    cmd.append(save_path)
    
    try:
        subprocess.run(cmd, check=True) 
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ FFmpeg failed with error code {e.returncode}")
        return False
    except Exception as e:
        print(f"❌ FFmpeg Error: {e}")
        return False

def download_with_engine(url: str, cookies: dict, user_agent: str, filename: str, format_type: str = "mp4") -> bool:
    """
    Main download logic. Decides whether to use FFmpeg or Requests.
    """
    if not url: return False

    save_path = f"downloads/{filename}"
    print(f"   [Downloader] Target: {save_path} ({format_type.upper()})")

    # 1. INITIAL CHECK: Is it obviously a stream?
    if is_hls_playlist(url, cookies, user_agent):
        print("   [Mode] Streaming Protocol Detected (Using FFmpeg)")
        return run_ffmpeg(url, cookies, user_agent, save_path, format_type)

    # 2. IF NOT, TRY DIRECT DOWNLOAD
    print("   [Mode] Direct File Download (Requests)")
    headers = {"User-Agent": user_agent}
    temp_file = "downloads/_temp_download.mp4"
    
    try:
        session = requests.Session()
        session.cookies.update(cookies)
        response = session.get(url, headers=headers, stream=True)
        response.raise_for_status()
        
        total = int(response.headers.get('content-length', 0))
        
        # --- HANDLE FAKE FILES (The "12kb" Problem) ---
        # If the file is tiny (< 25KB), it's likely a hidden playlist masking as an MP4.
        if total and total < 25000: 
            print("⚠️  Warning: File is too small. It's likely a hidden playlist.")
            print("   [Switching] Activating FFmpeg Engine...")
            response.close()
            # Stop direct download and force FFmpeg immediately
            return run_ffmpeg(url, cookies, user_agent, save_path, format_type)

        # Download the file chunk by chunk
        with open(temp_file, 'wb') as file, tqdm(total=total, unit='iB', unit_scale=True) as bar:
            for chunk in response.iter_content(chunk_size=1024):
                if chunk:
                    file.write(chunk)
                    bar.update(len(chunk))
        
        # Post-Processing: Convert to MP3 if requested
        if format_type == "mp3":
            print("   [Converting] Extracting MP3...")
            subprocess.run([
                'ffmpeg', '-y', '-i', temp_file, 
                '-vn', '-acodec', 'libmp3lame', '-q:a', '2', 
                save_path
            ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            os.remove(temp_file) # Clean up temp video
        else:
            if os.path.exists(save_path): os.remove(save_path)
            os.rename(temp_file, save_path)
            
        return True
        
    except Exception as e:
        print(f"❌ Direct Download Error: {e}")
        if os.path.exists(temp_file): os.remove(temp_file)
        return False