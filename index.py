#!/usr/bin/env python3
"""
YouTube Video Downloader using yt-dlp
Supports downloading videos in various formats and qualities
"""

import yt_dlp
import os
import sys
from pathlib import Path

class YouTubeDownloader:
    def __init__(self, download_path="./downloads"):
        """Initialize the downloader with a default download path"""
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        
    def download_video(self, url, quality="best", format_type="mp4"):
        """
        Download a YouTube video
        
        Args:
            url (str): YouTube video URL
            quality (str): Video quality - 'best', 'worst', or specific like '720p'
            format_type (str): Output format - 'mp4', 'webm', 'mkv', etc.
        """
        try:
            # Configure yt-dlp options
            ydl_opts = {
                'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
                'format': f'{quality}[ext={format_type}]/best[ext={format_type}]/best',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading: {url}")
                ydl.download([url])
                print("Download completed successfully!")
                
        except Exception as e:
            print(f"Error downloading video: {str(e)}")
            
    def download_audio_only(self, url, format_type="mp3"):
        """
        Download only audio from YouTube video
        
        Args:
            url (str): YouTube video URL
            format_type (str): Audio format - 'mp3', 'wav', 'aac', etc.
        """
        try:
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(self.download_path / '%(title)s.%(ext)s'),
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': format_type,
                    'preferredquality': '192',
                }],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading audio: {url}")
                ydl.download([url])
                print("Audio download completed successfully!")
                
        except Exception as e:
            print(f"Error downloading audio: {str(e)}")
            
    def get_video_info(self, url):
        """Get information about a YouTube video without downloading"""
        try:
            ydl_opts = {'quiet': True}
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                return {
                    'title': info.get('title', 'N/A'),
                    'duration': info.get('duration', 'N/A'),
                    'uploader': info.get('uploader', 'N/A'),
                    'view_count': info.get('view_count', 'N/A'),
                    'upload_date': info.get('upload_date', 'N/A')
                }
        except Exception as e:
            print(f"Error getting video info: {str(e)}")
            return None
            
    def download_playlist(self, playlist_url, quality="best", format_type="mp4"):
        """Download entire YouTube playlist"""
        try:
            ydl_opts = {
                'outtmpl': str(self.download_path / '%(playlist_title)s/%(title)s.%(ext)s'),
                'format': f'{quality}[ext={format_type}]/best[ext={format_type}]/best',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                print(f"Downloading playlist: {playlist_url}")
                ydl.download([playlist_url])
                print("Playlist download completed successfully!")
                
        except Exception as e:
            print(f"Error downloading playlist: {str(e)}")

def main():
    """Main function with interactive menu"""
    downloader = YouTubeDownloader()
    
    while True:
        print("\n" + "="*50)
        print("YouTube Video Downloader")
        print("="*50)
        print("1. Download video (MP4)")
        print("2. Download audio only (MP3)")
        print("3. Get video information")
        print("4. Download playlist")
        print("5. Custom download options")
        print("6. Exit")
        
        choice = input("\nSelect an option (1-6): ").strip()
        
        if choice == '1':
            url = input("Enter YouTube video URL: ").strip()
            if url:
                quality = input("Enter quality (best/worst/720p/480p/360p) [default: best]: ").strip() or "best"
                downloader.download_video(url, quality)
                
        elif choice == '2':
            url = input("Enter YouTube video URL: ").strip()
            if url:
                downloader.download_audio_only(url)
                
        elif choice == '3':
            url = input("Enter YouTube video URL: ").strip()
            if url:
                info = downloader.get_video_info(url)
                if info:
                    print(f"\nVideo Information:")
                    print(f"Title: {info['title']}")
                    print(f"Duration: {info['duration']} seconds")
                    print(f"Uploader: {info['uploader']}")
                    print(f"Views: {info['view_count']}")
                    print(f"Upload Date: {info['upload_date']}")
                    
        elif choice == '4':
            url = input("Enter YouTube playlist URL: ").strip()
            if url:
                quality = input("Enter quality (best/worst/720p/480p/360p) [default: best]: ").strip() or "best"
                downloader.download_playlist(url, quality)
                
        elif choice == '5':
            url = input("Enter YouTube video URL: ").strip()
            if url:
                quality = input("Enter quality (best/worst/720p/etc.) [default: best]: ").strip() or "best"
                format_type = input("Enter format (mp4/webm/mkv) [default: mp4]: ").strip() or "mp4"
                downloader.download_video(url, quality, format_type)
                
        elif choice == '6':
            print("Goodbye!")
            break
            
        else:
            print("Invalid choice. Please try again.")

# Example usage functions
def quick_download_example():
    """Quick download example"""
    downloader = YouTubeDownloader("./my_videos")
    
    # Download a single video
    video_url = "https://www.youtube.com/watch?v=VIDEO_ID"
    downloader.download_video(video_url, quality="720p")
    
    # Download audio only
    downloader.download_audio_only(video_url, format_type="mp3")
    
    # Get video info
    info = downloader.get_video_info(video_url)
    if info:
        print(f"Video title: {info['title']}")

if __name__ == "__main__":
    # Check if yt-dlp is installed
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp is not installed. Please install it using:")
        print("pip install yt-dlp")
        sys.exit(1)
    
    # Run the main interactive program
    main()