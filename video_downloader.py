import os
import time
import requests
import subprocess
from tqdm import tqdm
from urllib.parse import urlparse

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "*/*",
    "Connection": "keep-alive"
}

REFERER_MAP = {
    "twitter.com":     "https://twitter.com/",
    "x.com":           "https://twitter.com/",
    "tiktok.com":      "https://www.tiktok.com/",
    "instagram.com":   "https://www.instagram.com/",
    "vimeo.com":       "https://vimeo.com/",
    "dailymotion.com": "https://www.dailymotion.com/",
    "reddit.com":      "https://www.reddit.com/",
    "facebook.com":    "https://www.facebook.com/",
}

def format_duration(seconds: float) -> str:
    """Format seconds into MM:SS or H:MM:SS."""
    seconds = int(seconds)
    h = seconds // 3600
    m = (seconds % 3600) // 60
    s = seconds % 60
    if h > 0:
        return f"{h}:{m:02d}:{s:02d}"
    return f"{m:02d}:{s:02d}"

def get_referer_for_url(url: str) -> str | None:
    parsed = urlparse(url)
    hostname = parsed.hostname or ""
    for domain, referer in REFERER_MAP.items():
        if domain in hostname:
            return referer
    if parsed.scheme and parsed.netloc:
        return f"{parsed.scheme}://{parsed.netloc}/"
    return None

def get_headers_for_url(url: str, cookies: dict = {}, user_agent: str = None) -> dict:
    local_headers = HEADERS.copy()
    if user_agent:
        local_headers["User-Agent"] = user_agent
    if cookies:
        local_headers["Cookie"] = "; ".join([f"{k}={v}" for k, v in cookies.items()])
    referer = get_referer_for_url(url)
    if referer:
        local_headers["Referer"] = referer
    return local_headers

def get_hls_duration(m3u8_url: str, headers: dict) -> float:
    try:
        resp = requests.get(m3u8_url, headers=headers, timeout=10)
        total = 0.0
        for line in resp.text.splitlines():
            if line.startswith('#EXTINF:'):
                total += float(line.split(':')[1].split(',')[0])
        return total
    except Exception:
        return 0.0

def download_hls_stream(m3u8_url: str, cookies: dict, user_agent: str, filename: str) -> bool:
    folder_name = "downloads"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    output_path = os.path.join(folder_name, filename)

    if os.path.exists(output_path):
        print("⚠️  Partial file found. HLS streams can't be resumed — restarting.")
        os.remove(output_path)

    current_headers = get_headers_for_url(m3u8_url, cookies, user_agent)
    header_string = "".join([f"{k}: {v}\r\n" for k, v in current_headers.items()])

    print(f"🔄 Preparing download: {filename}")
    duration = get_hls_duration(m3u8_url, current_headers)
    if duration > 0:
        print(f"   Duration: {format_duration(duration)}")

    cmd = [
        'ffmpeg',
        '-allowed_extensions', 'ALL',
        '-headers', header_string,
        '-reconnect', '1',
        '-reconnect_streamed', '1',
        '-reconnect_delay_max', '15',
        '-i', m3u8_url,
        '-c', 'copy',
        '-bsf:a', 'aac_adtstoasc',
        '-progress', 'pipe:1',
        '-nostats',
        '-loglevel', 'error',
        output_path,
        '-y'
    ]

    try:
        process = subprocess.Popen(
            cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1
        )

        total_secs = int(duration) if duration > 0 else None
        total_label = format_duration(total_secs) if total_secs else "?"

        bar = tqdm(
            total=total_secs, unit='s', desc="⬇  Downloading", ncols=75,
            bar_format=f'{{desc}}: {{percentage:3.0f}}%|{{bar}}| {{n_fmt}}/{total_label} [{{elapsed}}<{{remaining}}] {{postfix}}'
        )

        last_pos = 0.0
        last_size_check = 0.0

        for line in process.stdout:
            key, _, value = line.strip().partition('=')
            if key == 'out_time_us':
                try:
                    current = float(value) / 1_000_000
                    delta = current - last_pos
                    if delta > 0:
                        bar.update(int(delta))
                        last_pos = current
                        # Update file size every 2 seconds
                        if current - last_size_check >= 2:
                            if os.path.exists(output_path):
                                size_mb = os.path.getsize(output_path) / (1024 * 1024)
                                bar.set_postfix_str(f"{size_mb:.1f} MB")
                            last_size_check = current
                except Exception:
                    pass
            elif key == 'progress' and value.strip() == 'end':
                if total_secs:
                    bar.n = total_secs
                bar.refresh()
                break

        process.wait()
        bar.close()

        if process.returncode != 0:
            err = process.stderr.read().strip()
            if err:
                print(f"❌ FFmpeg error: {err}")
            return False

        final_size = os.path.getsize(output_path) / (1024 * 1024) if os.path.exists(output_path) else 0
        print(f"✅ Saved to: {output_path} ({final_size:.1f} MB)")
        return True

    except FileNotFoundError:
        print("❌ FFmpeg is not installed.")
        return False
    except KeyboardInterrupt:
        print("\n⛔ Download cancelled.")
        bar.close()
        process.terminate()
        return False

def download_video_file(url: str, cookies: dict, user_agent: str, filename: str, max_retries: int = 15) -> bool:
    folder_name = "downloads"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    full_path = os.path.join(folder_name, filename)

    for attempt in range(max_retries):
        try:
            current_headers = get_headers_for_url(url, cookies, user_agent)

            existing_size = os.path.getsize(full_path) if os.path.exists(full_path) else 0
            if existing_size > 0:
                if attempt > 0:
                    print(f"\n🔄 Resuming from {existing_size / (1024*1024):.1f} MB (attempt {attempt+1})...")
                else:
                    print(f"⏩ Resuming from {existing_size / (1024*1024):.1f} MB...")
                current_headers["Range"] = f"bytes={existing_size}-"

            response = requests.get(url, stream=True, headers=current_headers, timeout=20)

            if response.status_code == 200 and existing_size > 0:
                print("⚠️  Server doesn't support resume. Restarting from beginning.")
                existing_size = 0
                current_headers.pop("Range", None)

            if response.status_code == 403:
                print(f"⚠️  403 Forbidden on attempt {attempt+1}. Retrying...")
                time.sleep(2)
                continue

            response.raise_for_status()

            total_size = int(response.headers.get('content-length', 0)) + existing_size
            total_mb = total_size / (1024 * 1024)
            mode = 'ab' if existing_size > 0 else 'wb'

            if total_mb > 0:
                print(f"   Total size: {total_mb:.1f} MB")

            with open(full_path, mode) as file, tqdm(
                desc="⬇  Downloading", total=total_size,
                initial=existing_size,
                unit='iB', unit_scale=True, unit_divisor=1024, ncols=75
            ) as bar:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        file.write(chunk)
                        bar.update(len(chunk))

            final_size = os.path.getsize(full_path) / (1024 * 1024)
            print(f"✅ Saved to: {full_path} ({final_size:.1f} MB)")
            return True

        except requests.exceptions.RequestException:
            print(f"\n⚠️  Connection dropped. Retrying in 5s... ({attempt+1}/{max_retries})")
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n⛔ Download cancelled. Run again to resume.")
            return False
        except Exception as e:
            print(f"\n⚠️  Attempt {attempt+1} failed: {e}")
            time.sleep(2)

    print("❌ All download attempts failed.")
    return False

def download_with_engine(url: str, cookies: dict, user_agent: str, filename: str, fmt: str) -> bool:
    if '.m3u8' in url.lower() or 'master.json' in url.lower():
        return download_hls_stream(url, cookies, user_agent, filename)
    else:
        return download_video_file(url, cookies, user_agent, filename)
