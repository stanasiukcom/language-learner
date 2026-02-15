#!/usr/bin/env python3
"""Configuration loader for Language Learner"""

import yaml
import os
from pathlib import Path
from typing import Dict, Any

class Config:
    """Configuration manager for Language Learner"""

    def __init__(self, config_path: str = None):
        """Load configuration from YAML file"""
        if config_path is None:
            # Look for config.yaml in config directory
            config_path = Path(__file__).parent.parent / "config" / "config.yaml"

        if not Path(config_path).exists():
            raise FileNotFoundError(
                f"Configuration file not found: {config_path}\n"
                "Please copy config/config.example.yaml to config/config.yaml and customize it."
            )

        with open(config_path, 'r', encoding='utf-8') as f:
            self.data = yaml.safe_load(f)

    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value using dot notation (e.g., 'course.name')"""
        keys = key.split('.')
        value = self.data

        for k in keys:
            if isinstance(value, dict):
                value = value.get(k)
            else:
                return default

            if value is None:
                return default

        return value

    def __getitem__(self, key: str) -> Any:
        """Allow dict-like access"""
        return self.get(key)

    @property
    def course_name(self) -> str:
        return self.get('course.name', 'Language Course')

    @property
    def language_code(self) -> str:
        return self.get('language.code', 'en')

    @property
    def native_language(self) -> str:
        return self.get('language.native_language', 'en')

    @property
    def output_dir(self) -> Path:
        return Path(self.get('output.directory', 'output'))

    @property
    def transcripts_dir(self) -> Path:
        return self.output_dir / self.get('output.transcripts_dir', 'transcripts')

    @property
    def audio_dir(self) -> Path:
        return self.output_dir / self.get('output.audio_dir', 'audio')

    def create_output_dirs(self):
        """Create necessary output directories"""
        self.output_dir.mkdir(exist_ok=True)
        self.transcripts_dir.mkdir(exist_ok=True)
        self.audio_dir.mkdir(exist_ok=True)
