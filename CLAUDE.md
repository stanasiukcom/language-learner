# CLAUDE.md - Development Guide for AI Assistants

This file provides context and guidelines for AI assistants (Claude, GPT, etc.) working on the Language Learner project.

---

## 🎯 Project Purpose

**Language Learner** is an automation tool that processes language course videos/audio into comprehensive study materials. It's designed to be:
- **Universal**: Works with any language
- **Automated**: Minimal manual intervention
- **Extensible**: Easy to add new features and languages
- **User-friendly**: Simple YAML configuration

---

## 🏗️ Architecture Overview

### Core Components

```
language-learner/
├── src/                        # Source code
│   ├── main.py                # Main CLI entry point
│   ├── config_loader.py       # YAML config parser
│   ├── downloader.py          # Multi-source video downloader
│   ├── transcriber.py         # Whisper transcription
│   ├── notes_generator.py     # Markdown notes generator
│   ├── resources_db.py        # Language-specific resources
│   └── progress_tracker.py    # Resumable processing
├── config/                     # Configuration files
│   ├── config.example.yaml    # Template configuration
│   └── config.yaml            # User's actual config (gitignored)
├── examples/                   # Example configurations
├── scripts/                    # Utility scripts
└── docs/                       # Additional documentation
```

### Data Flow

```
Video Sources → Download → Extract Audio → Transcribe → Generate Notes
                  ↓            ↓             ↓            ↓
              video.mp4    audio.mp3    transcript.txt  notes.md
                                            + .json
```

---

## 🔧 Common Development Tasks

### Adding Support for a New Language

1. **Add alphabet info** (if non-Latin script):
   ```python
   # In src/resources_db.py - _init_alphabets()
   'ko': """<a name="alphabet"></a>
   ## 🔤 Korean Alphabet (한글/Hangul)

   24 letters (14 consonants, 10 vowels)

   | Letter | Sound | Notes |
   |--------|-------|-------|
   | ㄱ | g/k | like 'g' in 'go' |
   # ... more letters
   """
   ```

2. **Add learning resources**:
   ```python
   # In src/resources_db.py - _init_resources()
   def _get_korean_resources(self) -> str:
       return """## 🌟 Korean Learning Resources

       ### 📱 Apps
       - Talk To Me In Korean
       - LingoDeer Korean

       ### 🎥 YouTube
       - Korean Unnie
       - Learn Korean with GO! Billy Korean
       """

   # Then add to _init_resources() dict:
   'ko': self._get_korean_resources(),
   ```

3. **Test with sample config**:
   ```yaml
   # config/korean_example.yaml
   language:
     code: "ko"
     native_language: "en"
     script: "Hangul"
   ```

### Improving Transcription Accuracy

**For specific languages:**
```python
# In src/transcriber.py - transcribe() method

# Add language-specific preprocessing
if self.language == 'ar':
    # Arabic-specific audio processing
    pass
elif self.language == 'ja':
    # Japanese-specific settings
    pass
```

**For better timestamps:**
```python
# Enable word-level timestamps
result = self.model.transcribe(
    str(audio_path),
    language=self.language,
    verbose=True,
    word_timestamps=True  # More granular timestamps
)
```

### Adding New Download Sources

**Example: Adding Zoom recording support:**

```python
# In src/downloader.py

def download_zoom(self, recording_id: str, output_filename: str) -> bool:
    """Download from Zoom cloud recordings"""
    try:
        # Implement Zoom API integration
        url = f"https://zoom.us/rec/download/{recording_id}"
        # ... download logic
        return True
    except Exception as e:
        logger.error(f"Zoom download error: {e}")
        return False

# In download_lessons() method, add:
elif source_type == 'zoom':
    recording_id = lesson.get('id')
    if self.download_zoom(recording_id, filename):
        downloaded_files.append(filename)
```

### Enhancing Notes Generation

**Adding vocabulary extraction:**

```python
# In src/notes_generator.py

def _extract_vocabulary(self, segments: List[Dict]) -> List[Dict]:
    """Extract vocabulary with context"""
    vocab = []

    for seg in segments:
        # Look for patterns like "X means Y" or "X is called Y"
        patterns = [
            r'(\w+)\s+means\s+(\w+)',
            r'(\w+)\s+is called\s+(\w+)',
            # Add language-specific patterns
        ]

        for pattern in patterns:
            matches = re.findall(pattern, seg['text'])
            for match in matches:
                vocab.append({
                    'word': match[0],
                    'translation': match[1],
                    'timestamp': seg['start'],
                    'context': seg['text']
                })

    return vocab
```

**Adding quiz generation:**

```python
def _generate_quiz(self, vocabulary: List[Dict]) -> str:
    """Generate practice quiz from vocabulary"""
    quiz = "## 📝 Practice Quiz\n\n"

    for i, item in enumerate(vocabulary[:20], 1):
        quiz += f"{i}. What does '{item['word']}' mean?\n"
        quiz += f"   - Answer: {item['translation']}\n\n"

    return quiz
```

---

## 🧪 Testing Guidelines

### Manual Testing Workflow

1. **Test download:**
   ```bash
   python src/main.py --download-only -c config/test_config.yaml
   ```

2. **Test transcription:**
   ```bash
   python src/main.py --transcribe-only -c config/test_config.yaml
   ```

3. **Test notes generation:**
   ```bash
   python src/main.py --notes-only -c config/test_config.yaml
   ```

4. **Full pipeline:**
   ```bash
   python src/main.py -c config/test_config.yaml
   ```

### Creating Test Fixtures

```python
# tests/test_transcriber.py
import unittest
from pathlib import Path
from src.transcriber import Transcriber

class TestTranscriber(unittest.TestCase):
    def test_format_timestamp(self):
        result = Transcriber._format_timestamp(3665)
        self.assertEqual(result, "01:01:05")

    def test_extract_audio(self):
        # Use small test video (5 seconds)
        transcriber = Transcriber(model="tiny")
        # ... test implementation
```

---

## 🎨 Code Style Guidelines

### Python Style

- **PEP 8** compliant
- Type hints for function signatures
- Docstrings for all public methods
- Descriptive variable names

```python
def transcribe(self, audio_path: Path, output_path: Path,
               json_path: Optional[Path] = None) -> Dict:
    """
    Transcribe audio file using Whisper.

    Args:
        audio_path: Path to input audio file
        output_path: Path for text transcript output
        json_path: Optional path for JSON output with timestamps

    Returns:
        Dict containing transcript text and metadata
    """
    # Implementation
```

### Configuration Design

- Use clear, hierarchical YAML structure
- Provide sensible defaults
- Comment all non-obvious options

```yaml
# Good:
transcription:
  model: "medium"  # Options: tiny, base, small, medium, large
  language: "ar"   # ISO 639-1 code or auto-detect with null

# Bad:
trans_mdl: "med"
lang: "arabic"
```

---

## 🚀 Feature Ideas & Roadmap

### High Priority
- [ ] Anki flashcard export (.apkg format)
- [ ] Notion integration (auto-create study pages)
- [ ] PDF export with proper formatting
- [ ] Speaker diarization (identify different speakers)
- [ ] Multiple native language support for notes

### Medium Priority
- [ ] Web UI (Flask/FastAPI)
- [ ] Docker containerization
- [ ] Batch processing with queue system
- [ ] Custom vocabulary extraction models
- [ ] Grammar pattern recognition

### Low Priority
- [ ] Mobile app companion
- [ ] Cloud processing API
- [ ] Spaced repetition scheduler
- [ ] Community resource sharing

### Integration Ideas
- **Anki**: Export vocabulary as flashcards
- **Notion**: Auto-create study database
- **Obsidian**: Generate interconnected notes
- **Quizlet**: Export study sets
- **Google Sheets**: Vocabulary tracking

---

## 🔍 Debugging Tips

### Common Issues

**Whisper model download fails:**
```python
# Manually specify cache dir
os.environ['WHISPER_CACHE'] = '/path/to/cache'
model = whisper.load_model("medium", download_root='/path/to/cache')
```

**Encoding errors in non-Latin scripts:**
```python
# Always use UTF-8 encoding
with open(file, 'r', encoding='utf-8') as f:
    content = f.read()
```

**Progress tracking not working:**
```python
# Add debug logging
logger.info(f"Completed tasks: {self.progress.data['completed']}")
logger.info(f"Checking task: {task_id}")
```

---

## 📦 Dependencies Explained

### Core Dependencies
- **openai-whisper**: Speech-to-text transcription
- **pyyaml**: Configuration file parsing
- **yt-dlp**: Universal video downloader

### System Dependencies
- **ffmpeg**: Audio/video processing
- **poppler**: PDF support (future feature)

### Optional Dependencies
- **torch**: GPU acceleration for Whisper
- **pandas**: Data processing (future)
- **beautifulsoup4**: Web scraping resources (future)

---

## 🤖 AI Assistant Guidelines

### When Working on This Project:

1. **Understand the user's language**: Check config for target language and native language
2. **Preserve existing functionality**: Don't break working features
3. **Follow the architecture**: Keep separation of concerns
4. **Test changes**: Provide testing instructions
5. **Update documentation**: Keep README and this file in sync
6. **Consider edge cases**: Different scripts, RTL languages, long videos

### Helpful Prompts for Users

When users want to add features:
```
"I'll help you add [feature] to Language Learner. First, let me understand:
1. Which component does this affect? (downloader/transcriber/notes_generator)
2. Is this language-specific or universal?
3. Do you need example code or full implementation?"
```

### Code Generation Best Practices

- Generate complete, working code (not pseudocode)
- Include error handling
- Add logging statements
- Provide usage examples
- Update relevant config files

---

## 📚 Resources for Contributors

### Learning Whisper API
- https://github.com/openai/whisper
- https://platform.openai.com/docs/guides/speech-to-text

### YAML Best Practices
- https://yaml.org/spec/1.2.2/
- https://yamllint.readthedocs.io/

### Language Codes
- ISO 639-1: https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
- Whisper supported languages: 99+ languages

---

## ✅ Pull Request Checklist

Before submitting PRs:
- [ ] Code follows PEP 8 style
- [ ] All functions have docstrings
- [ ] Changes tested manually
- [ ] README updated if needed
- [ ] Example config added (if new feature)
- [ ] No breaking changes (or documented)
- [ ] Logging added for debugging

---

## 💡 Pro Tips

1. **Performance**: Process videos overnight for large courses
2. **Quality**: Use `large` Whisper model for critical content
3. **Storage**: Delete video files after transcription if space-limited
4. **Batch processing**: Use shell scripts for multiple courses
5. **Customization**: Fork and customize `notes_generator.py` for your needs

---

**Remember**: This tool is meant to help language learners focus on learning, not on manual note-taking. Keep the user experience simple and the automation robust!

---

*Last updated: 2026-02-15*
*Maintained by: Language Learner Community*
