#!/usr/bin/env python3
"""
Audio transcription using Whisper or other engines
"""

import subprocess
import json
from pathlib import Path
from typing import Optional, Dict
import logging
import whisper

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class Transcriber:
    """Transcribe audio/video files"""

    def __init__(self, model: str = "medium", language: str = None):
        self.model_name = model
        self.language = language
        self.model = None

    def load_model(self):
        """Load Whisper model (lazy loading)"""
        if self.model is None:
            logger.info(f"Loading Whisper '{self.model_name}' model...")
            self.model = whisper.load_model(self.model_name)
            logger.info("✓ Model loaded")

    def extract_audio(self, video_path: Path, audio_path: Path) -> bool:
        """Extract audio from video using ffmpeg"""
        try:
            logger.info(f"Extracting audio from {video_path.name}...")

            cmd = [
                "ffmpeg", "-i", str(video_path),
                "-vn",  # No video
                "-acodec", "libmp3lame",
                "-y",  # Overwrite
                str(audio_path)
            ]

            result = subprocess.run(cmd, capture_output=True, text=True)

            if result.returncode != 0:
                logger.error(f"Audio extraction failed: {result.stderr}")
                return False

            logger.info(f"✓ Audio extracted: {audio_path.name}")
            return True

        except Exception as e:
            logger.error(f"Error extracting audio: {e}")
            return False

    def transcribe(self, audio_path: Path, output_path: Path,
                   json_path: Optional[Path] = None) -> Dict:
        """Transcribe audio file"""
        try:
            self.load_model()

            logger.info(f"Transcribing {audio_path.name}...")
            logger.info("This may take 10-20 minutes for a 1.5-hour audio file...")

            result = self.model.transcribe(
                str(audio_path),
                language=self.language,
                verbose=True,
                word_timestamps=False
            )

            # Save text transcript
            logger.info(f"Saving transcript to {output_path}...")
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(f"Transcription - {audio_path.stem}\n")
                f.write("=" * 70 + "\n\n")
                f.write("FULL TRANSCRIPT:\n")
                f.write("-" * 70 + "\n")
                f.write(result["text"])
                f.write("\n\n" + "=" * 70 + "\n\n")

                # Timestamped segments
                f.write("TIMESTAMPED TRANSCRIPT:\n")
                f.write("-" * 70 + "\n\n")

                for segment in result.get("segments", []):
                    timestamp = self._format_timestamp(segment["start"])
                    text = segment["text"].strip()
                    f.write(f"[{timestamp}] {text}\n")

                duration = result.get('duration', 0)
                f.write(f"\nDuration: {self._format_timestamp(duration)}\n")
                f.write(f"Segments: {len(result.get('segments', []))}\n")

            # Save JSON with full data
            if json_path:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(result, f, ensure_ascii=False, indent=2)
                logger.info(f"✓ JSON data saved: {json_path}")

            logger.info(f"✓ Transcript saved: {output_path}")
            return result

        except Exception as e:
            logger.error(f"Transcription error: {e}")
            return {}

    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """Convert seconds to HH:MM:SS format"""
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = int(seconds % 60)
        return f"{hours:02d}:{minutes:02d}:{secs:02d}"
