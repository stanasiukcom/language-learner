#!/usr/bin/env python3
"""
Video downloader supporting multiple sources
"""

import subprocess
import sys
from pathlib import Path
from typing import Dict, List
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class VideoDownloader:
    """Download videos from various sources"""

    def __init__(self, output_dir: Path):
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

    def download_google_drive(self, file_id: str, output_filename: str) -> bool:
        """Download from Google Drive using yt-dlp"""
        try:
            url = f"https://drive.google.com/file/d/{file_id}/view"
            output_path = self.output_dir / output_filename

            logger.info(f"Downloading from Google Drive: {output_filename}")

            cmd = ["yt-dlp", url, "-o", str(output_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                logger.error(f"Download failed: {result.stderr}")
                return False

            logger.info(f"✓ Downloaded: {output_filename}")
            return True

        except Exception as e:
            logger.error(f"Error downloading {output_filename}: {e}")
            return False

    def download_youtube(self, video_id: str, output_filename: str) -> bool:
        """Download from YouTube"""
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            output_path = self.output_dir / output_filename

            logger.info(f"Downloading from YouTube: {output_filename}")

            cmd = ["yt-dlp", url, "-o", str(output_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                logger.error(f"Download failed: {result.stderr}")
                return False

            logger.info(f"✓ Downloaded: {output_filename}")
            return True

        except Exception as e:
            logger.error(f"Error downloading {output_filename}: {e}")
            return False

    def download_url(self, url: str, output_filename: str) -> bool:
        """Download from direct URL"""
        try:
            output_path = self.output_dir / output_filename

            logger.info(f"Downloading from URL: {output_filename}")

            cmd = ["yt-dlp", url, "-o", str(output_path)]
            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                # Fallback to curl
                cmd = ["curl", "-L", url, "-o", str(output_path)]
                result = subprocess.run(cmd, capture_output=True, text=True)

                if result.returncode != 0:
                    logger.error(f"Download failed: {result.stderr}")
                    return False

            logger.info(f"✓ Downloaded: {output_filename}")
            return True

        except Exception as e:
            logger.error(f"Error downloading {output_filename}: {e}")
            return False

    def download_lessons(self, lessons: List[Dict], source_type: str) -> List[str]:
        """Download multiple lessons"""
        downloaded_files = []

        for lesson in lessons:
            filename = lesson.get('filename')

            if source_type == 'google_drive':
                file_id = lesson.get('id')
                if self.download_google_drive(file_id, filename):
                    downloaded_files.append(filename)

            elif source_type == 'youtube':
                video_id = lesson.get('id')
                if self.download_youtube(video_id, filename):
                    downloaded_files.append(filename)

            elif source_type == 'url':
                url = lesson.get('url')
                if self.download_url(url, filename):
                    downloaded_files.append(filename)

            elif source_type == 'local':
                # Just verify file exists
                if (self.output_dir / filename).exists():
                    downloaded_files.append(filename)
                    logger.info(f"✓ Found local file: {filename}")
                else:
                    logger.warning(f"✗ Local file not found: {filename}")

        return downloaded_files
