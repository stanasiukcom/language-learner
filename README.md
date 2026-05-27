# 🌍 Language Learner

**Automated language course processing: Download → Transcribe → Generate Comprehensive Notes**

Automate your language learning workflow for any language. Download lesson videos, extract audio, transcribe with timestamps, and generate comprehensive study notes with external resources.

---

## ✨ Features

- 📥 **Multi-source Download**: Google Drive, YouTube, direct URLs
- 🎙️ **Auto-Transcription**: OpenAI Whisper with timestamps
- 📝 **Smart Notes**: Auto-generated comprehensive study materials
- 📱 **Tablet-Friendly PDFs**: Beautiful, readable PDFs optimized for tablets
- 🌐 **Multi-Language**: Arabic, Japanese, Chinese, Spanish, French, German, Russian, and more
- 📚 **Resource Database**: Curated apps, YouTube channels, websites per language
- 🔄 **Resumable**: Progress tracking for interrupted processing
- ⚙️ **Configurable**: YAML configuration for any course structure

---

## 🚀 Quick Start

### 1. Installation

This project uses [**uv**](https://docs.astral.sh/uv/) for Python environment and dependency management.

```bash
# Install uv (if you don't have it)
brew install uv                              # macOS
# or: curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/stanasiukcom/language-learner.git
cd language-learner

# Create .venv and install all Python dependencies (reads pyproject.toml + uv.lock)
uv sync

# Install system dependencies (macOS)
brew install ffmpeg poppler pango gdk-pixbuf glib

# Or Linux (Ubuntu/Debian)
sudo apt-get install ffmpeg poppler-utils python3-cffi python3-brotli libpango-1.0-0 libgdk-pixbuf2.0-0
```

> `uv sync` is idempotent — re-run it any time the lockfile or `pyproject.toml` changes. You don't need to `pip install` anything separately. To activate the venv interactively, use `source .venv/bin/activate`; otherwise prefix commands with `uv run`.

### 2. Configuration

**⚠️ IMPORTANT: Your config files are automatically gitignored and will NOT be committed.**

```bash
# Copy example config
cp config/config.example.yaml config/config.yaml

# Edit config.yaml with your course details
nano config/config.yaml
```

**Privacy Note:** Configuration files may contain private Google Drive IDs and personal course information. The `.gitignore` is configured to exclude all `config/*.yaml` files except the example template.

**Minimal configuration:**
```yaml
course:
  name: "Spanish A1"
  language: "Spanish"
  level: "Beginner"

language:
  code: "es"
  native_language: "en"

sources:
  - type: "google_drive"
    lessons:
      - id: "YOUR_GOOGLE_DRIVE_FILE_ID"
        filename: "lesson1.mp4"
        date: "2024-01-15"
```

### 3. Run

```bash
# Process everything automatically
uv run python src/main.py

# Or step-by-step:
uv run python src/main.py --download-only    # Download videos
uv run python src/main.py --transcribe-only  # Transcribe
uv run python src/main.py --notes-only       # Generate notes
```

> Already activated the venv with `source .venv/bin/activate`? You can drop the `uv run` prefix and call `python src/main.py` directly.

### 4. Results

```
output/
├── lesson1.mp4                           # Downloaded video
├── audio/
│   └── lesson1.mp3                       # Extracted audio
├── transcripts/
│   ├── lesson1.txt                       # Text transcript
│   └── lesson1.json                      # JSON with timestamps
├── Comprehensive_Notes_Spanish_A1.md     # 📖 YOUR STUDY GUIDE (Markdown)
└── Comprehensive_Notes_Spanish_A1.pdf    # 📱 TABLET-FRIENDLY VERSION
```

---

## 📚 Supported Languages

| Language | Code | Alphabet | Resources |
|----------|------|----------|-----------|
| Arabic | ar | ✅ | ✅ |
| Chinese | zh | ✅ | ✅ |
| Japanese | ja | ✅ | ✅ |
| Russian | ru | ✅ | ✅ |
| Spanish | es | ➖ | ✅ |
| French | fr | ➖ | ✅ |
| German | de | ➖ | ✅ |
| **Any language** | xx | Manual | Template |

Don't see your language? Contributions welcome! See [CLAUDE.md](CLAUDE.md) for adding new languages.

---

## 🎯 Use Cases

### For Students
- Automate processing of online course recordings
- Generate searchable, timestamped notes
- Access curated resources for your target language
- Track progress with built-in checklists

### For Teachers
- Create study materials from lecture recordings
- Share comprehensive notes with students
- Maintain course content library

### For Self-Learners
- Process YouTube courses/playlists
- Build personal study guides
- Discover quality learning resources

---

## ⚙️ Configuration Guide

### Video Sources

**Google Drive:**
```yaml
sources:
  - type: "google_drive"
    lessons:
      - id: "1abc123xyz"  # From drive.google.com/file/d/1abc123xyz/view
        filename: "lesson1.mp4"
        date: "2024-01-15"
```

**YouTube:**
```yaml
sources:
  - type: "youtube"
    lessons:
      - id: "dQw4w9WgXcQ"  # From youtube.com/watch?v=dQw4w9WgXcQ
        filename: "lesson1.mp4"
```

**Direct URL:**
```yaml
sources:
  - type: "url"
    lessons:
      - url: "https://example.com/video.mp4"
        filename: "lesson1.mp4"
```

**Local Files:**
```yaml
sources:
  - type: "local"
    lessons:
      - filename: "lesson1.mp4"  # Already in output/ directory
```

### Whisper Models

| Model | Speed | Accuracy | Use Case |
|-------|-------|----------|----------|
| tiny | ⚡️⚡️⚡️ | ⭐️ | Testing |
| base | ⚡️⚡️ | ⭐️⭐️ | Quick drafts |
| small | ⚡️ | ⭐️⭐️⭐️ | Good balance |
| **medium** | 🐌 | ⭐️⭐️⭐️⭐️ | **Recommended** |
| large | 🐌🐌 | ⭐️⭐️⭐️⭐️⭐️ | Best quality |

---

## 🛠️ Advanced Usage

### PDF Generation

PDFs are automatically generated alongside Markdown notes. They feature:
- **Tablet-optimized formatting** - Perfect for iPad, Android tablets
- **Beautiful typography** - Readable fonts and spacing
- **Syntax highlighting** - For code blocks and examples
- **Table support** - Clean, professional tables
- **RTL support** - For Arabic, Hebrew, etc.

Disable PDF generation:
```yaml
notes:
  generate_pdf: false
```

### Custom Note Templates

Edit `src/notes_generator.py` to customize note structure.

### Add New Language Resources

1. Edit `src/resources_db.py`
2. Add your language code to `_init_resources()`
3. Create resource list with apps, YouTube, websites
4. Submit PR!

### Parallel Processing

```yaml
advanced:
  parallel_processing: true  # Process multiple videos simultaneously
```

**⚠️ Warning:** High CPU and memory usage!

---

## 🤝 Contributing

We welcome contributions! See [CLAUDE.md](CLAUDE.md) for:
- Adding new languages
- Improving transcription accuracy
- Enhancing note generation
- Adding integrations (Anki, Notion, etc.)

---

## 📖 Examples

See `examples/` directory for:
- `arabic_config.yaml` - Arabic course example
- `japanese_config.yaml` - Japanese course example
- `output_sample.md` - Sample generated notes

---

## 🐛 Troubleshooting

### "yt-dlp: command not found"
`yt-dlp` is installed inside the project's `.venv` by `uv sync`. Either prefix commands with `uv run` (e.g. `uv run yt-dlp ...`) or activate the venv (`source .venv/bin/activate`). If you want a system-wide yt-dlp, `brew install yt-dlp`.

### "ffmpeg: command not found"
```bash
brew install ffmpeg       # macOS
sudo apt install ffmpeg   # Linux
```

### Google Drive download fails
- Ensure files are publicly accessible or shared with you
- Get shareable link, extract file ID
- File ID is between `/d/` and `/view` in URL

### Transcription is slow
- Use smaller Whisper model (`small` instead of `medium`)
- Process shorter videos
- Use GPU if available (requires CUDA setup)

### Out of memory
- Use smaller Whisper model
- Process videos one at a time
- Close other applications

---

## 📄 License

MIT License - See [LICENSE](LICENSE) file

---

## 🙏 Acknowledgments

- [OpenAI Whisper](https://github.com/openai/whisper) - Speech recognition
- [yt-dlp](https://github.com/yt-dlp/yt-dlp) - Video downloader
- [FFmpeg](https://ffmpeg.org/) - Audio extraction

---

## 📞 Support

- 🐛 Issues: [GitHub Issues](https://github.com/stanasiukcom/language-learner/issues)
- 💬 Discussions: [GitHub Discussions](https://github.com/stanasiukcom/language-learner/discussions)
- ⭐ Star the repo: [github.com/stanasiukcom/language-learner](https://github.com/stanasiukcom/language-learner)

---

**Made with ❤️ for language learners worldwide**

⭐️ Star this repo if you find it useful!
