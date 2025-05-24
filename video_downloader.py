#!/usr/bin/env python3
"""
Combined Video Downloader (Hacker Edition)
Downloads videos from YouTube, YouTube Playlists, Instagram, TikTok, Twitter/X, Facebook, Reddit, Pinterest, and Snapchat.
Features a hacker-style interface with green text and enhanced banners.
Requires yt-dlp, instaloader, requests, ffmpeg, and uuid.
"""

import os
import sys
import re
from pathlib import Path
import yt_dlp
import instaloader
import requests
from urllib.parse import urlparse
import time
import uuid

# ANSI escape codes for green text
GREEN = "\033[32m"
RESET = "\033[0m"

class VideoDownloader:
    def __init__(self, download_path="./downloads"):
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)

        # Base YouTube downloader options
        self.yt_ydl_opts = {
            'format': 'bestvideo[height<=2160]+bestaudio/best',
            'outtmpl': str(self.download_path / '%(platform)s_%(title)s_%(id)s.%(ext)s'),
            'merge_output_format': 'mp4',
            'postprocessors': [
                {'key': 'FFmpegVideoConvertor', 'preferedformat': 'mp4'},
                {'key': 'FFmpegMetadata'},
            ],
            'noplaylist': True,
            'quiet': False,
            'no_warnings': True,
            'ignoreerrors': False,
            'retries': 3,
            'socket_timeout': 30,
        }

    def validate_youtube_url(self, url):
        youtube_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(watch\?v=|embed/|v/|shorts/|.+\?v=)?([^&=%\?]{11})'
        )
        return youtube_regex.match(url) is not None

    def validate_youtube_playlist_url(self, url):
        playlist_regex = re.compile(
            r'(https?://)?(www\.)?(youtube|youtu|youtube-nocookie)\.(com|be)/'
            r'(playlist\?list=|watch\?v=.*&list=)([a-zA-Z0-9_-]+)'
        )
        return playlist_regex.match(url) is not None

    def validate_instagram_url(self, url):
        instagram_regex = re.compile(
            r'(https?://)?(www\.)?instagram\.com/(p|reel)/([^/]+)/'
        )
        return instagram_regex.match(url) is not None

    def validate_tiktok_url(self, url):
        tiktok_regex = re.compile(
            r'(https?://)?(www\.)?(tiktok\.com|vm\.tiktok\.com)/(@[^/]+/video/\d+|t/\w+)'
        )
        return tiktok_regex.match(url) is not None

    def validate_twitter_url(self, url):
        twitter_regex = re.compile(
            r'(https?://)?(www\.)?(x\.com|twitter\.com)/[^/]+/status/\d+'
        )
        return twitter_regex.match(url) is not None

    def validate_facebook_url(self, url):
        facebook_regex = re.compile(
            r'(https?://)?(www\.)?(facebook\.com|fb\.watch)/.+'
        )
        return facebook_regex.match(url) is not None

    def validate_reddit_url(self, url):
        reddit_regex = re.compile(
            r'(https?://)?(www\.)?reddit\.com/r/[^/]+/comments/[^/]+'
        )
        return reddit_regex.match(url) is not None

    def validate_pinterest_url(self, url):
        pinterest_regex = re.compile(
            r'(https?://)?(www\.)?pinterest\.com/pin/\d+'
        )
        return pinterest_regex.match(url) is not None

    def validate_snapchat_url(self, url):
        snapchat_regex = re.compile(
            r'(https?://)?(www\.)?snapchat\.com/add/[^/]+/[^/]+'
        )
        return snapchat_regex.match(url) is not None

    def download_youtube_video(self, url, quality_choice, is_playlist=False):
        if not (self.validate_youtube_url(url) or (is_playlist and self.validate_youtube_playlist_url(url))):
            print(f"{GREEN}❌ Invalid YouTube {'Playlist' if is_playlist else 'Video'} URL!{RESET}")
            return False

        quality_map = {
            '1': 'bestvideo[height<=2160]+bestaudio/best',  # 4K
            '2': 'bestvideo[height<=1440]+bestaudio/best',  # 1440P
            '3': 'bestvideo[height<=1080]+bestaudio/best',  # 1080P
            '4': 'bestvideo+bestaudio/best',                # BEST
            '5': 'bestaudio[ext=m4a]/bestaudio',           # AUDIO
        }

        ydl_opts = self.yt_ydl_opts.copy()
        ydl_opts['format'] = quality_map.get(quality_choice, quality_map['1'])
        ydl_opts['outtmpl'] = str(self.download_path / f'youtube_%(title)s_{uuid.uuid4().hex[:8]}.%(ext)s')
        ydl_opts['noplaylist'] = not is_playlist
        if quality_choice == '5':
            ydl_opts['postprocessors'] = [
                {'key': 'FFmpegExtractAudio', 'preferredcodec': 'mp3', 'preferredquality': '192'},
                {'key': 'FFmpegMetadata'},
            ]
            ydl_opts.pop('merge_output_format', None)

        max_retries = 3
        for attempt in range(max_retries):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    print(f"{GREEN}🎬 Title: {info.get('title')}{RESET}")
                    print(f"{GREEN}👤 Uploader: {info.get('uploader')}{RESET}")
                    ydl.download([url])
                self.print_thank_you_banner()
                return True
            except yt_dlp.utils.DownloadError as e:
                print(f"{GREEN}Attempt {attempt + 1}: Download failed: {e}{RESET}")
                if attempt < max_retries - 1:
                    print(f"{GREEN}Retrying in 5 seconds...{RESET}")
                    time.sleep(5)
                continue
            except Exception as e:
                print(f"{GREEN}Attempt {attempt + 1}: An error occurred: {e}{RESET}")
                if attempt < max_retries - 1:
                    print(f"{GREEN}Retrying in 5 seconds...{RESET}")
                    time.sleep(5)
                continue
        print(f"{GREEN}❌ Failed to download YouTube {'Playlist' if is_playlist else 'Video'} after {max_retries} attempts.{RESET}")
        return False

    def download_youtube_playlist(self, url, quality_choice):
        return self.download_youtube_video(url, quality_choice, is_playlist=True)

    def download_instagram_video(self, url, username=None, password=None):
        if not self.validate_instagram_url(url):
            print(f"{GREEN}❌ Invalid Instagram URL!{RESET}")
            return False

        L = instaloader.Instaloader(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
                       "(KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        )

        session_file = "instagram_session"
        if username and os.path.exists(session_file):
            try:
                L.load_session_from_file(username, session_file)
                print(f"{GREEN}Loaded Instagram session from file.{RESET}")
            except Exception as e:
                print(f"{GREEN}Failed to load session: {e}{RESET}")

        if username and password and not L.context.is_logged_in:
            try:
                L.login(username, password)
                L.save_session_to_file(session_file)
                print(f"{GREEN}Logged in to Instagram successfully and saved session.{RESET}")
            except Exception as e:
                print(f"{GREEN}Instagram login failed: {e}{RESET}")
                return False

        try:
            shortcode = urlparse(url).path.split('/')[-2]
            print(f"{GREEN}Extracted Instagram shortcode: {shortcode}{RESET}")
            post = instaloader.Post.from_shortcode(L.context, shortcode)

            if not post.is_video:
                print(f"{GREEN}❌ The provided URL does not contain a video.{RESET}")
                return False

            video_url = post.video_url
            if not video_url:
                print(f"{GREEN}❌ Could not retrieve Instagram video URL.{RESET}")
                return False

            filename = self.download_path / f"instagram_{shortcode}_{uuid.uuid4().hex[:8]}.mp4"
            max_retries = 3
            for attempt in range(max_retries):
                try:
                    response = requests.get(video_url, stream=True, timeout=10)
                    if response.status_code == 200:
                        with open(filename, 'wb') as f:
                            for chunk in response.iter_content(chunk_size=8192):
                                if chunk:
                                    f.write(chunk)
                        print(f"{GREEN}✅ Instagram video downloaded successfully as {filename}{RESET}")
                        print(f"{GREEN}Note: If 1080p is unavailable, the highest available resolution was downloaded.{RESET}")
                        self.print_thank_you_banner()
                        return True
                    else:
                        print(f"{GREEN}Attempt {attempt + 1}: Failed to download video. Status code: {response.status_code}{RESET}")
                except requests.exceptions.RequestException as e:
                    print(f"{GREEN}Attempt {attempt + 1}: Connection error: {e}{RESET}")
                    if attempt < max_retries - 1:
                        print(f"{GREEN}Retrying in 5 seconds...{RESET}")
                        time.sleep(5)
                    continue
            print(f"{GREEN}❌ Failed to download Instagram video after multiple attempts.{RESET}")
            return False

        except instaloader.exceptions.ConnectionException as e:
            print(f"{GREEN}❌ Connection error: {e}{RESET}")
            print(f"{GREEN}This may be due to rate limits or network issues. Try again later or use a VPN.{RESET}")
            return False
        except instaloader.exceptions.InvalidArgumentException:
            print(f"{GREEN}❌ Invalid Instagram post URL or shortcode.{RESET}")
            return False
        except instaloader.exceptions.LoginRequiredException:
            print(f"{GREEN}❌ Login is required to access this post. Please provide username and password.{RESET}")
            return False
        except Exception as e:
            print(f"{GREEN}❌ An unexpected error occurred: {e}{RESET}")
            return False

    def download_generic_video(self, url, platform, is_playlist=False, cookies_file=None):
        if not getattr(self, f'validate_{platform.lower()}_url')(url):
            print(f"{GREEN}❌ Invalid {platform} URL!{RESET}")
            return False

        ydl_opts = self.yt_ydl_opts.copy()
        ydl_opts['outtmpl'] = str(self.download_path / f'{platform.lower()}_%(title)s_{uuid.uuid4().hex[:8]}.%(ext)s')
        ydl_opts['noplaylist'] = not is_playlist
        if cookies_file and os.path.exists(cookies_file):
            ydl_opts['cookiefile'] = cookies_file
        else:
            print(f"{GREEN}Note: No cookies file provided. Attempting download without authentication, which may fail for restricted content.{RESET}")

        max_retries = 3
        for attempt in range(max_retries):
            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(url, download=False)
                    print(f"{GREEN}🎬 Title: {info.get('title')}{RESET}")
                    print(f"{GREEN}👤 Uploader: {info.get('uploader') or 'Unknown'}{RESET}")
                    ydl.download([url])
                self.print_thank_you_banner()
                return True
            except yt_dlp.utils.DownloadError as e:
                print(f"{GREEN}Attempt {attempt + 1}: Download failed: {e}{RESET}")
                if attempt < max_retries - 1:
                    print(f"{GREEN}Retrying in 5 seconds...{RESET}")
                    time.sleep(5)
                continue
            except Exception as e:
                print(f"{GREEN}Attempt {attempt + 1}: An error occurred: {e}{RESET}")
                if attempt < max_retries - 1:
                    print(f"{GREEN}Retrying in 5 seconds...{RESET}")
                    time.sleep(5)
                continue
        print(f"{GREEN}❌ Failed to download {platform} video after {max_retries} attempts.{RESET}")
        print(f"{GREEN}Note: For {platform}, ensure a valid cookies file is provided for private or restricted content. Try using a VPN or checking your network connection for timeouts.{RESET}")
        return False

    def print_thank_you_banner(self):
        print(f"{GREEN}")
        print("╔════════════════════════════════════════════╗")
        print("║                                            ║")
        print("║               THANK YOU                    ║")
        print("║               Dev by izu x n4              ║")
        print("║                                            ║")
        print("╚════════════════════════════════════════════╝")
        print(f"{RESET}")

def print_hacker_banner():
    print(f"{GREEN}")
    print("╔═══════════════════════════════════════════════════╗")
    print("║                                                   ║")
    print("║           Dev by: IZU x N4                        ║")
    print("║  just breaking the rules, nothing else!           ║")
    print("║                                                   ║")
    print("╚═══════════════════════════════════════════════════╝")
    print(f"{RESET}")

def main():
    downloader = VideoDownloader()
    while True:
        print_hacker_banner()
        print(f"{GREEN}Choose platform\n1. YOUTUBE\n2. YOUTUBE PLAYLIST\n3. INSTAGRAM\n4. TIKTOK\n5. TWITTER/X\n6. FACEBOOK\n7. REDDIT\n8. PINTEREST\n9. SNAPCHAT\n10. EXIT\n➠ {RESET}", end="")
        platform = input().strip()

        cookies_file = None
        if platform in ["5", "6", "9"]:  # Twitter/X, Facebook, Snapchat
            print(f"{GREEN}Enter path to cookies file (or press Enter to skip): {RESET}", end="")
            cookies_file = input().strip() or None
            if cookies_file and not os.path.exists(cookies_file):
                print(f"{GREEN}❌ Cookies file does not exist: {cookies_file}{RESET}")
                cookies_file = None

        if platform == "1":
            print(f"{GREEN}Enter YouTube video URL: {RESET}", end="")
            url = input().strip()
            print(f"{GREEN}Select quality\n1. 4K\n2. 1440P\n3. 1080P\n4. BEST\n5. AUDIO\n➠ {RESET}", end="")
            quality = input().strip()
            downloader.download_youtube_video(url, quality)
        elif platform == "2":
            print(f"{GREEN}Enter YouTube playlist URL: {RESET}", end="")
            url = input().strip()
            print(f"{GREEN}Select quality\n1. 4K\n2. 1440P\n3. 1080P\n4. BEST\n5. AUDIO\n➠ {RESET}", end="")
            quality = input().strip()
            downloader.download_youtube_playlist(url, quality)
        elif platform == "3":
            print(f"{GREEN}Enter Instagram video URL: {RESET}", end="")
            url = input().strip()
            print(f"{GREEN}Enter Instagram username (or press Enter to skip): {RESET}", end="")
            username = input().strip() or None
            password = None
            if username:
                print(f"{GREEN}Enter Instagram password (or press Enter to skip): {RESET}", end="")
                password = input().strip() or None
            downloader.download_instagram_video(url, username, password)
        elif platform == "4":
            print(f"{GREEN}Enter TikTok video URL: {RESET}", end="")
            url = input().strip()
            downloader.download_generic_video(url, "tiktok")
        elif platform == "5":
            print(f"{GREEN}Enter Twitter/X video URL: {RESET}", end="")
            url = input().strip()
            downloader.download_generic_video(url, "twitter", cookies_file=cookies_file)
        elif platform == "6":
            print(f"{GREEN}Enter Facebook video URL: {RESET}", end="")
            url = input().strip()
            downloader.download_generic_video(url, "facebook", cookies_file=cookies_file)
        elif platform == "7":
            print(f"{GREEN}Enter Reddit video URL: {RESET}", end="")
            url = input().strip()
            downloader.download_generic_video(url, "reddit")
        elif platform == "8":
            print(f"{GREEN}Enter Pinterest video URL: {RESET}", end="")
            url = input().strip()
            downloader.download_generic_video(url, "pinterest")
        elif platform == "9":
            print(f"{GREEN}Enter Snapchat video URL: {RESET}", end="")
            url = input().strip()
            downloader.download_generic_video(url, "snapchat", cookies_file=cookies_file)
        elif platform == "10":
            print(f"{GREEN}👋 Exiting IZU x N4 Video Downloader. Stay hacking!{RESET}")
            break
        else:
            print(f"{GREEN}❌ Invalid platform! Please enter 1-10.{RESET}")

        print(f"{GREEN}Do you want to download another video? (y/n): {RESET}", end="")
        if input().strip().lower() != 'y':
            print(f"{GREEN}👋 Exiting IZU x N4 Video Downloader. Stay hacking!{RESET}")
            break

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{GREEN}👋 Interrupted by user. Exiting IZU x N4 Video Downloader.{RESET}")
        sys.exit(0)
    except Exception as e:
        print(f"{GREEN}❌ Unexpected error: {e}{RESET}")
        sys.exit(1)