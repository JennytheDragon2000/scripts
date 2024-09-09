import sys
import subprocess
import tempfile
import os
import yt_dlp

def get_video_info(url):
    ydl_opts = {
        'proxy': 'http://127.0.0.1:8889',
        'format': 'best[height<=720]',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
        return info['url']

def take_screenshot(video_url, timestamp):
    with tempfile.NamedTemporaryFile(suffix='.png', delete=False) as temp_file:
        screenshot_path = temp_file.name

    mpv_command = [
        'mpv',
        '--start=' + timestamp,
        '--frames=1',
        '--no-audio',
        '--no-terminal',
        '--screenshot-format=png',
        '--screenshot-png-compression=0',
        f'--screenshot-template={screenshot_path}',
        '--screenshot-sw',
        video_url
    ]

    subprocess.run(mpv_command, check=True)
    return screenshot_path

def copy_to_clipboard(image_path):
    subprocess.run(['xclip', '-selection', 'clipboard', '-t', 'image/png', '-i', image_path], check=True)

def main():
    if len(sys.argv) != 3:
        print("Usage: python script.py <youtube_url> <timestamp>")
        sys.exit(1)

    url = sys.argv[1]
    timestamp = sys.argv[2]

    try:
        video_url = get_video_info(url)
        screenshot_path = take_screenshot(video_url, timestamp)
        copy_to_clipboard(screenshot_path)
        print("Screenshot copied to clipboard successfully!")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'screenshot_path' in locals():
            os.unlink(screenshot_path)

if __name__ == "__main__":
    main()
