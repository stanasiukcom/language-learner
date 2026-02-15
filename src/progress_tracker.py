#!/usr/bin/env python3
"""Progress tracking for resumable processing"""

import json
from pathlib import Path
from datetime import datetime
from typing import Set

class ProgressTracker:
    """Track processing progress for resumability"""

    def __init__(self, progress_file: Path):
        self.progress_file = Path(progress_file)
        self.data = self._load()

    def _load(self) -> dict:
        """Load progress from JSON file"""
        if self.progress_file.exists():
            with open(self.progress_file, 'r') as f:
                return json.load(f)
        return {
            'completed': [],
            'started': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }

    def _save(self):
        """Save progress to JSON file"""
        self.data['last_updated'] = datetime.now().isoformat()
        with open(self.progress_file, 'w') as f:
            json.dump(self.data, f, indent=2)

    def mark_completed(self, task_id: str):
        """Mark a task as completed"""
        if task_id not in self.data['completed']:
            self.data['completed'].append(task_id)
            self._save()

    def is_completed(self, task_id: str) -> bool:
        """Check if a task is completed"""
        return task_id in self.data['completed']

    def reset(self):
        """Reset all progress"""
        self.data = {
            'completed': [],
            'started': datetime.now().isoformat(),
            'last_updated': datetime.now().isoformat()
        }
        self._save()
