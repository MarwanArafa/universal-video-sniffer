import json
import time
import re
import requests
from typing import Tuple, Dict, Optional

COMMON_HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
}

def clean_filename(title: str) -> str:
    clean = re.sub(r'[\\/*?:"<>|]', "", title)
    return clean[:100].strip()

def resolve_best_hls(master_url: str, session: requests.Session) -> str:
    """Given a master.m3u8, fetch it and return the highest bandwidth index playlist URL."""
    try:
        r = session.get(master_url, timeout=10)
        lines = r.text.splitlines()
        best_url = None
        best_bw = 0
        for i, line in enumerate(lines):
            if line.startswith('#EXT-X-STREAM-INF'):
                match = re.search(r'BANDWIDTH=(\d+)', line)
                bw = int(match.group(1)) if match else 0
                if bw >= best_bw and i + 1 < len(lines):
                    next_line = lines[i + 1].strip()
                    if next_line and not next_line.startswith('#'):
                        best_bw = bw
                        if next_line.startswith('http'):
                            best_url = next_line
                        else:
                            base = master_url.rsplit('/', 1)[0]
                            best_url = f"{base}/{next_line}"
        return best_url or master_url
    except:
        return master_url

def extract_flashvars_site(url: str) -> Tuple[Optional[str], Dict, str, str]:
    from urllib.parse import urlparse
    parsed = urlparse(url)
    origin = f"{parsed.scheme}://{parsed.netloc}/"

    session = requests.Session()
    session.headers.update({**COMMON_HEADERS, "Referer": origin})

    resp = session.get(url, timeout=15)
    html = resp.text

    title_match = re.search(r'<title>(.+?)</title>', html)
    title = clean_filename(title_match.group(1)) if title_match else "downloaded_video"
    # Strip common site name suffixes from title (e.g. " - SiteName.com")
    title = re.sub(r'\s*-\s*\S+\.\w{2,}$', '', title).strip()

    flashvars_match = re.search(r'var flashvars_\d+\s*=\s*(\{.+?\});', html, re.DOTALL)
    if not flashvars_match:
        print("   [Sniffer] Could not find flashvars in page source.")
        return None, {}, "mp4", title

    try:
        flashvars = json.loads(flashvars_match.group(1))
    except json.JSONDecodeError:
        print("   [Sniffer] Could not parse flashvars JSON.")
        return None, {}, "mp4", title

    media_defs = flashvars.get("mediaDefinitions", [])
    cookies = {c.name: c.value for c in session.cookies}

    # Prefer HLS — resolve master into best quality index playlist
    for item in media_defs:
        if item.get("format") == "hls":
            master_url = item.get("videoUrl") or item.get("defaultQuality")
            if master_url:
                best_url = resolve_best_hls(master_url, session)
                print(f"   [Sniffer] 🎯 FOUND HLS: {best_url[:60]}...")
                return best_url, cookies, COMMON_HEADERS["User-Agent"], title

    # Fallback: highest quality direct MP4
    mp4_items = [i for i in media_defs if i.get("videoUrl", "").endswith(".mp4")]
    if mp4_items:
        best = sorted(mp4_items, key=lambda x: int(x.get("quality", 0) or 0), reverse=True)[0]
        mp4_url = best["videoUrl"]
        print(f"   [Sniffer] 🎯 FOUND MP4: {mp4_url[:60]}...")
        return mp4_url, cookies, COMMON_HEADERS["User-Agent"], title

    print("   [Sniffer] No usable media found in flashvars.")
    return None, {}, "mp4", title

# ---------------------------------------------------------------------------
# Selenium fallback for unknown sites
# ---------------------------------------------------------------------------

VIDEO_SIGNALS = [".m3u8", "master.json", ".mp4", ".webm", "googlevideo.com", "video.twimg.com"]
URL_BLACKLIST  = [".js", ".css", ".png", ".jpg", ".gif", ".svg", ".ico", "favicon",
                  "preview", "thumbnail", "sprite", "seek", "analytics", "tracking",
                  "beacon", "pixel", "ads", "static", "www-static"]

def is_video_url(url: str) -> bool:
    u = url.lower()
    return any(s in u for s in VIDEO_SIGNALS) and not any(b in u for b in URL_BLACKLIST)

def extract_with_selenium(webpage_url: str) -> Tuple[Optional[str], Dict, str, str]:
    try:
        from selenium import webdriver
        from selenium.webdriver.chrome.options import Options
        from selenium.webdriver.chrome.service import Service
        from webdriver_manager.chrome import ChromeDriverManager
    except ImportError:
        print("❌ Selenium not installed.")
        return None, {}, "", "downloaded_video"

    print("   [Sniffer] Using Selenium fallback (headless browser)...")

    options = Options()
    options.add_argument('--headless=new')
    options.add_argument('--mute-audio')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1280,720')
    options.add_argument('--blink-settings=imagesEnabled=false')
    options.add_argument('--disable-blink-features=AutomationControlled')
    options.add_experimental_option('excludeSwitches', ['enable-automation'])
    options.add_experimental_option('useAutomationExtension', False)
    options.set_capability('goog:loggingPrefs', {'performance': 'ALL'})

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.execute_cdp_cmd('Page.addScriptToEvaluateOnNewDocument', {
        'source': "Object.defineProperty(navigator, 'webdriver', {get: () => undefined})"
    })

    video_url = None
    cookies = {}
    video_title = "downloaded_video"
    user_agent = driver.execute_script("return navigator.userAgent")

    try:
        driver.get(webpage_url)
        time.sleep(6)
        if driver.title:
            video_title = clean_filename(driver.title)
            print(f"   [Sniffer] Detected Title: {video_title}")

        for script in [
            "document.querySelector('video') && document.querySelector('video').play()",
            "window.scrollTo(0, 300)",
        ]:
            try: driver.execute_script(script)
            except: pass

        start_time = time.time()
        while time.time() - start_time < 60:
            try: driver.execute_script("document.querySelector('video') && document.querySelector('video').play()")
            except: pass

            for entry in driver.get_log('performance'):
                try:
                    msg = json.loads(entry['message'])['message']
                    if msg['method'] != 'Network.requestWillBeSent': continue
                    url = msg['params']['request']['url']
                    if not is_video_url(url): continue
                    if ".m3u8" in url or "master.json" in url:
                        video_url = url
                        print(f"   [Sniffer] 🎯 FOUND: {url[:60]}...")
                        break
                    if not video_url:
                        video_url = url
                        print(f"   [Sniffer] Candidate: {url[:60]}...")
                except: continue

            if video_url and (".m3u8" in video_url or "master.json" in video_url): break
            if video_url and (time.time() - start_time > 15): break
            time.sleep(1)

        if video_url:
            cookies = {c['name']: c['value'] for c in driver.get_cookies()}

    except Exception as e:
        print(f"   [Sniffer] Selenium error: {e}")
    finally:
        driver.quit()

    return video_url, cookies, user_agent, video_title

# ---------------------------------------------------------------------------
# Main router — add new site extractors here in the future
# ---------------------------------------------------------------------------

FLASHVARS_DOMAINS = [
    "pornhub.com",
    "redtube.com",
    "youporn.com",
    "tube8.com",
]

SITE_EXTRACTORS = {domain: extract_flashvars_site for domain in FLASHVARS_DOMAINS}

def print_runtime_warning():
    print("\n" + "="*60)
    print("   🔍  Scanning for video stream...")
    print("="*60 + "\n")

def extract_media_data(webpage_url: str) -> Tuple[Optional[str], Dict, str, str]:
    print(f"   [Sniffer] Target: {webpage_url}")
    print_runtime_warning()

    for domain, extractor in SITE_EXTRACTORS.items():
        if domain in webpage_url:
            print(f"   [Sniffer] Using fast extractor...")
            return extractor(webpage_url)

    return extract_with_selenium(webpage_url)
