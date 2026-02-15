#!/usr/bin/env python3
"""
Generate comprehensive study notes from transcripts
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List
import logging

from config_loader import Config
from resources_db import ResourcesDatabase

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class NotesGenerator:
    """Generate comprehensive study notes"""

    def __init__(self, config: Config):
        self.config = config
        self.resources_db = ResourcesDatabase()

    def generate(self, output_path: Path):
        """Generate complete notes file"""
        logger.info("Analyzing transcripts and generating notes...")

        content = []

        # Header
        content.append(self._generate_header())

        # Alphabet section (if non-Latin script)
        if self.config.get('notes.include_alphabet', True):
            alphabet = self.resources_db.get_alphabet(self.config.language_code)
            if alphabet:
                content.append(alphabet)

        # Lesson sections
        lessons = self.config.get('sources.0.lessons', [])
        for i, lesson in enumerate(lessons, 1):
            content.append(self._generate_lesson_section(i, lesson))

        # Resources section
        if self.config.get('notes.include_resources', True):
            content.append(self._generate_resources_section())

        # Footer
        content.append(self._generate_footer())

        # Save
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))

        logger.info(f"✓ Notes generated: {len(''.join(content))} characters")

    def _generate_header(self) -> str:
        """Generate notes header"""
        lang = self.config.get('course.language', 'Language')
        level = self.config.get('course.level', 'A1')
        institution = self.config.get('course.institution', '')

        return f"""# 📚 Comprehensive {lang} Study Notes - {level}
**{institution if institution else 'Language Course'}**

*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*

---

## 📖 Table of Contents

1. [Introduction](#introduction)
2. [Alphabet](#alphabet)
3. [Lessons](#lessons)
4. [Resources](#resources)
5. [Study Tips](#study-tips)

---

<a name="introduction"></a>
## 🎯 Introduction

These comprehensive notes include:
- ✅ Lesson transcripts with timestamps
- ✅ Vocabulary with translations
- ✅ Grammar explanations
- ✅ Practice exercises
- ✅ Extensive external resources

**💡 How to use:**
- Timestamps **[HH:MM:SS]** link to video moments
- Review lessons systematically
- Use external resources for practice
- Track progress with checklists

---
"""

    def _generate_lesson_section(self, lesson_num: int, lesson: Dict) -> str:
        """Generate section for one lesson"""
        date = lesson.get('date', '')
        title = lesson.get('title', f'Lesson {lesson_num}')
        filename = lesson.get('filename', '')

        # Load transcript JSON if exists
        json_path = self.config.transcripts_dir / filename.replace('.mp4', '.json')

        section = f"""
<a name="lesson-{lesson_num}"></a>
## 📅 Lesson {lesson_num} - {date}
### {title}

"""

        if json_path.exists():
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)

            # Analyze transcript
            analysis = self._analyze_transcript(data)

            # Add sections
            if analysis.get('vocabulary'):
                section += "#### 📚 Vocabulary\n\n"
                for item in analysis['vocabulary'][:15]:
                    section += f"- **[{item['time']}]** {item['text'][:100]}...\n"
                section += "\n"

            if analysis.get('grammar'):
                section += "#### 📖 Grammar\n\n"
                for item in analysis['grammar'][:10]:
                    section += f"**[{item['time']}]**\n> {item['text'][:150]}...\n\n"

        section += f"\n📹 **Video:** {filename}\n\n---\n"

        return section

    def _analyze_transcript(self, data: Dict) -> Dict:
        """Analyze transcript to extract learning points"""
        segments = data.get('segments', [])

        # Simple keyword-based extraction
        vocab_keywords = ['word', 'means', 'called', 'vocabulary', 'słowo', 'oznacza']
        grammar_keywords = ['grammar', 'rule', 'form', 'gramatyka', 'zasada']

        vocab = []
        grammar = []

        for seg in segments:
            text = seg['text'].lower()
            timestamp = self._format_timestamp(seg['start'])

            if any(kw in text for kw in vocab_keywords):
                vocab.append({'time': timestamp, 'text': seg['text'].strip()})
            elif any(kw in text for kw in grammar_keywords):
                grammar.append({'time': timestamp, 'text': seg['text'].strip()})

        return {'vocabulary': vocab, 'grammar': grammar}

    def _generate_resources_section(self) -> str:
        """Generate external resources section"""
        lang_code = self.config.language_code
        native_lang = self.config.native_language

        resources = self.resources_db.get_resources(lang_code, native_lang)

        if not resources:
            return "\n## 🌟 External Resources\n\n*Resources not yet available for this language.*\n"

        return resources

    def _generate_footer(self) -> str:
        """Generate notes footer"""
        return f"""
---

## ✅ Progress Checklist

### Week 1-2: Basics
- [ ] Learn the alphabet/script
- [ ] Master basic greetings
- [ ] Learn numbers 1-10
- [ ] Practice pronunciation daily

### Month 1: Foundation
- [ ] 100+ vocabulary words
- [ ] Basic grammar rules
- [ ] Simple conversations
- [ ] Daily 15-minute practice

### Month 2-3: Development
- [ ] 300+ vocabulary words
- [ ] Understand verb conjugations
- [ ] Watch content with subtitles
- [ ] Join language exchange

---

*Generated by Language Learner - Automated Language Study Tool*
*Repository: https://github.com/yourusername/language-learner*
"""

    @staticmethod
    def _format_timestamp(seconds: float) -> str:
        """Convert seconds to HH:MM:SS"""
        h = int(seconds // 3600)
        m = int((seconds % 3600) // 60)
        s = int(seconds % 60)
        return f"{h:02d}:{m:02d}:{s:02d}"
