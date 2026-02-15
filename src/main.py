#!/usr/bin/env python3
"""
Language Learner - Main Processor
Automates: Download → Transcribe → Generate Notes
"""

import argparse
import sys
from pathlib import Path
import logging

from config_loader import Config
from downloader import VideoDownloader
from transcriber import Transcriber
from notes_generator import NotesGenerator
from progress_tracker import ProgressTracker

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class LanguageLearner:
    """Main processor for language learning materials"""

    def __init__(self, config_path: str = None):
        self.config = Config(config_path)
        self.config.create_output_dirs()
        self.progress = ProgressTracker(self.config.output_dir / "progress.json")

    def process_all(self):
        """Main processing pipeline"""
        logger.info("="*70)
        logger.info(f"Language Learner - {self.config.course_name}")
        logger.info("="*70)

        # Step 1: Download videos
        if self.config.get('sources'):
            self._download_videos()

        # Step 2: Extract audio and transcribe
        lessons = self.config.get('sources.0.lessons', [])
        for lesson in lessons:
            filename = lesson.get('filename')
            date = lesson.get('date')

            if self.progress.is_completed(f"transcribe_{filename}"):
                logger.info(f"✓ Already processed: {filename}")
                continue

            self._process_lesson(filename, date)
            self.progress.mark_completed(f"transcribe_{filename}")

        # Step 3: Generate comprehensive notes
        if not self.progress.is_completed("generate_notes"):
            self._generate_notes()
            self.progress.mark_completed("generate_notes")

        logger.info("\n" + "="*70)
        logger.info("✅ All processing completed!")
        logger.info("="*70)
        logger.info(f"📖 Notes file: {self.config.output_dir / self._get_notes_filename()}")

    def _download_videos(self):
        """Download all videos from configured sources"""
        logger.info("\n📥 Downloading videos...")

        downloader = VideoDownloader(self.config.output_dir)

        for source in self.config.get('sources', []):
            if not source.get('enabled', True):
                continue

            source_type = source.get('type')
            lessons = source.get('lessons', [])

            downloaded = downloader.download_lessons(lessons, source_type)
            logger.info(f"✓ Downloaded {len(downloaded)} files from {source_type}")

    def _process_lesson(self, video_filename: str, date: str):
        """Process a single lesson: extract audio and transcribe"""
        video_path = self.config.output_dir / video_filename
        audio_filename = video_filename.replace('.mp4', '.mp3')
        audio_path = self.config.audio_dir / audio_filename

        transcript_filename = video_filename.replace('.mp4', '.txt')
        transcript_path = self.config.transcripts_dir / transcript_filename
        json_path = self.config.transcripts_dir / video_filename.replace('.mp4', '.json')

        # Extract audio
        if self.config.get('processing.extract_audio', True):
            transcriber = Transcriber(
                model=self.config.get('transcription.model', 'medium'),
                language=self.config.get('language.code')
            )

            if not audio_path.exists():
                if not transcriber.extract_audio(video_path, audio_path):
                    logger.error(f"Failed to extract audio from {video_filename}")
                    return

        # Transcribe
        if not transcript_path.exists():
            transcriber = Transcriber(
                model=self.config.get('transcription.model', 'medium'),
                language=self.config.get('language.code')
            )
            transcriber.transcribe(audio_path, transcript_path, json_path)

        # Cleanup
        if not self.config.get('processing.keep_video', True):
            video_path.unlink()
            logger.info(f"✓ Cleaned up: {video_filename}")

    def _generate_notes(self):
        """Generate comprehensive study notes"""
        logger.info("\n📝 Generating comprehensive notes...")

        generator = NotesGenerator(self.config)
        notes_filename = self._get_notes_filename()
        output_path = self.config.output_dir / notes_filename

        generator.generate(output_path)

        logger.info(f"✓ Notes generated: {notes_filename}")

    def _get_notes_filename(self) -> str:
        """Get formatted notes filename"""
        template = self.config.get('output.notes_filename',
                                  'Comprehensive_Notes_{language}_{level}.md')
        return template.format(
            language=self.config.get('course.language', 'Language'),
            level=self.config.get('course.level', 'A1')
        ).replace(' ', '_')

def main():
    """Command-line interface"""
    parser = argparse.ArgumentParser(
        description='Language Learner - Automate language course processing'
    )
    parser.add_argument(
        '-c', '--config',
        default='config/config.yaml',
        help='Path to configuration file'
    )
    parser.add_argument(
        '--download-only',
        action='store_true',
        help='Only download videos'
    )
    parser.add_argument(
        '--transcribe-only',
        action='store_true',
        help='Only transcribe existing videos'
    )
    parser.add_argument(
        '--notes-only',
        action='store_true',
        help='Only generate notes from existing transcripts'
    )

    args = parser.parse_args()

    try:
        learner = LanguageLearner(args.config)

        if args.download_only:
            learner._download_videos()
        elif args.transcribe_only:
            lessons = learner.config.get('sources.0.lessons', [])
            for lesson in lessons:
                learner._process_lesson(lesson['filename'], lesson['date'])
        elif args.notes_only:
            learner._generate_notes()
        else:
            learner.process_all()

    except FileNotFoundError as e:
        logger.error(str(e))
        sys.exit(1)
    except Exception as e:
        logger.error(f"Error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()
