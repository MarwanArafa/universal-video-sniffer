import json
import time
import re
from typing import Tuple, Dict, Optional

try:
    from selenium import webdriver
    from selenium.webdriver.chrome.options import Options
    from selenium.webdriver.chrome.service import Service
    from webdriver_manager.chrome import ChromeDriverManager
except ImportError:
    print("❌ Error: Selenium not installed. Run: pip install selenium webdriver-manager")
    exit(1)

def print_runtime_warning():
    """Prints a massive warning when the browser is about to open."""
    print("\n" + "!"*60)
    print("      ⚠️   BROWSER IS OPENING - DO NOT CLOSE IT   ⚠️")
    print("!"*60)
    print("   1. A Chrome window will appear shortly.")
    print("   2. IGNORE the 'Chrome is being controlled by software' warning.")
    print("   3. YOU MUST INTERACT WITH THE PAGE:")
    print("      👉 Click 'Accept Cookies' or close popups immediately.")
    print("      👉 Click the video 'PLAY' button if it doesn't start.")
    print("   4. The script is watching. Once the video starts, it will")
    print("      close the window automatically.")
    print("!"*60 + "\n")

def clean_filename(title: str) -> str:
    """Removes bad characters from the title to make it a safe filename."""
    # Remove things like | / : ? * < > " which are illegal in filenames
    clean = re.sub(r'[\\/*?:"<>|]', "", title)
    # limit length to 100 chars to avoid filesystem errors
    return clean[:100].strip()

def extract_media_data(webpage_url: str) -> Tuple[Optional[str], Dict, str, str]:
    print(f"   [Sniffer] Launching browser to scan: {webpage_url}")
    print_runtime_warning()

    options = Options()
    options.add_argument('--mute-audio')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.set_window_size(1280, 720)

    video_url = None
    cookies = {}
    video_title = "downloaded_video" # Default fallback
    user_agent = driver.execute_script("return navigator.userAgent")

    try:
        driver.get(webpage_url)
        
        # --- WAIT FOR TITLE ---
        # We grab the page title (browser tab name) which usually matches the video
        time.sleep(3) 
        if driver.title:
            video_title = clean_filename(driver.title)
            print(f"   [Sniffer] Detected Title: {video_title}")

        print("   [Sniffer] ⏳ Waiting for video traffic... (Please clear ads/popups)")
        
        start_time = time.time()
        while time.time() - start_time < 60:
            try:
                driver.execute_script("document.querySelector('video').play()")
            except:
                pass

            logs = driver.get_log('performance')
            for entry in logs:
                try:
                    message = json.loads(entry['message'])['message']
                    if message['method'] != 'Network.requestWillBeSent': continue
                    url = message['params']['request']['url']
                    
                    if not any(x in url for x in [".m3u8", ".mp4", "googlevideo.com", "master.json", ".ts", "video.twimg.com"]): continue
                    if any(bad in url for bad in [".png", ".jpg", "favicon", "rs:fit", "preview", "thumbnails", "seek", "sprite"]): continue
                    
                    if ".m3u8" in url or "master.json" in url:
                        video_url = url
                        print(f"   [Sniffer] 🎯 FOUND MASTER PLAYLIST: {url[:60]}...")
                        break
                    
                    if not video_url:
                        video_url = url
                        print(f"   [Sniffer] Found potential video: {url[:60]}...")     
                except:
                    continue
            
            if video_url and (".m3u8" in video_url or "master.json" in video_url): break
            if video_url and (time.time() - start_time > 15): break

            time.sleep(1) 
            
        if video_url:
            selenium_cookies = driver.get_cookies()
            for cookie in selenium_cookies:
                cookies[cookie['name']] = cookie['value']

    except Exception as e:
        print(f"   [Sniffer] Error during scan: {e}")
    finally:
        driver.quit()

    # RETURN 4 THINGS NOW (Added Title)
    return video_url, cookies, user_agent, video_title