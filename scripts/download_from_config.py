#!/usr/bin/env python3
"""
Download all lessons listed in a Language Learner config file.

Usage: python scripts/download_from_config.py [config_path]
"""

import sys
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from downloader import VideoDownloader  # noqa: E402


def main() -> int:
    config_path = Path(sys.argv[1]) if len(sys.argv) > 1 else PROJECT_ROOT / "config" / "arabic_ar1_maciek.yaml"
    if not config_path.is_absolute():
        config_path = PROJECT_ROOT / config_path

    with open(config_path, encoding="utf-8") as f:
        config = yaml.safe_load(f)

    videos_dir = PROJECT_ROOT / config.get("paths", {}).get("videos_dir", "output/videos")
    cookies_browser = config.get("advanced", {}).get("cookies_browser")

    downloader = VideoDownloader(videos_dir, cookies_browser=cookies_browser)

    total = 0
    succeeded = []
    for source in config.get("sources", []):
        source_type = source.get("type")
        lessons = source.get("lessons", [])
        total += len(lessons)
        succeeded.extend(downloader.download_lessons(lessons, source_type))

    print(f"\nDownloaded {len(succeeded)}/{total} files to {videos_dir}")
    return 0 if len(succeeded) == total else 1


if __name__ == "__main__":
    sys.exit(main())
