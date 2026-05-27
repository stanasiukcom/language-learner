# 🚀 Quick Start Guide

Get started with Language Learner in 5 minutes.

---

## Step 1: Install Dependencies

Python dependencies are managed with [**uv**](https://docs.astral.sh/uv/).

### macOS
```bash
# Install uv + system libraries
brew install uv ffmpeg poppler pango gdk-pixbuf glib

# Create .venv and install all Python dependencies
uv sync
```

### Linux (Ubuntu/Debian)
```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# System dependencies
sudo apt-get update
sudo apt-get install ffmpeg poppler-utils \
  python3-cffi python3-brotli libpango-1.0-0 libgdk-pixbuf2.0-0

# Create .venv and install all Python dependencies
uv sync
```

### Windows
```bash
# Install uv (PowerShell)
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"

# System dependencies
choco install ffmpeg

# Create .venv and install all Python dependencies
uv sync
```

> `uv sync` creates `.venv/` in the project root and installs everything from `pyproject.toml` / `uv.lock`. Run `source .venv/bin/activate` to use it interactively, or prefix every command with `uv run`.

---

## Step 2: Configure Your Course

```bash
# Copy example configuration
cp config/config.example.yaml config/config.yaml

# Edit with your course details
nano config/config.yaml
```

**Minimal config example:**
```yaml
course:
  name: "Spanish A1"
  language: "Spanish"
  level: "Beginner"

language:
  code: "es"
  native_language: "en"

sources:
  - type: "youtube"
    lessons:
      - id: "VIDEO_ID_HERE"
        filename: "lesson1.mp4"
        date: "2024-01-15"
```

---

## Step 3: Run Processing

### Full Pipeline (Recommended for first time)
```bash
uv run python src/main.py
```

This will:
1. ⬇️  Download all videos
2. 🎙️  Extract audio and transcribe
3. 📝  Generate comprehensive study notes

### Step-by-Step (Optional)
```bash
# Download only
uv run python src/main.py --download-only

# Transcribe only
uv run python src/main.py --transcribe-only

# Generate notes only
uv run python src/main.py --notes-only

# Use custom config file
uv run python src/main.py -c config/my_config.yaml
```

> If you ran `source .venv/bin/activate`, drop the `uv run` prefix.

---

## Step 4: Access Your Notes

```
output/
├── lesson1.mp4                           # Downloaded video
├── audio/
│   └── lesson1.mp3                       # Extracted audio
├── transcripts/
│   ├── lesson1.txt                       # Text transcript
│   └── lesson1.json                      # JSON with timestamps
└── Comprehensive_Notes_[Language].md     # 📖 YOUR STUDY GUIDE
```

---

## Common Use Cases

### YouTube Playlist
```yaml
sources:
  - type: "youtube"
    lessons:
      - id: "dQw4w9WgXcQ"
        filename: "lesson1.mp4"
```

### Google Drive (Public Files)
```yaml
sources:
  - type: "google_drive"
    lessons:
      - id: "1abc123xyz"  # From: drive.google.com/file/d/1abc123xyz/view
        filename: "lesson1.mp4"
```

### Local Files (Already Downloaded)
```yaml
sources:
  - type: "local"
    lessons:
      - filename: "my_video.mp4"  # Must be in output/ directory
```

---

## Troubleshooting

### "ffmpeg: command not found"
```bash
# macOS
brew install ffmpeg

# Linux
sudo apt install ffmpeg
```

### "yt-dlp: command not found"
`yt-dlp` ships with this project's venv. Use `uv run yt-dlp ...` or activate the venv (`source .venv/bin/activate`). If `uv sync` didn't install it, re-run `uv sync`.

### Google Drive download fails
- Ensure file is publicly accessible
- Get shareable link
- Extract file ID from URL: `drive.google.com/file/d/FILE_ID_HERE/view`

### Transcription is slow
- Use smaller Whisper model: `model: "small"` instead of `"medium"`
- Process shorter videos
- Use GPU if available

---

## Next Steps

📖 **Full Documentation**: See [README.md](README.md)

🔧 **Configuration Guide**: See examples in `examples/` directory

🤖 **For Developers**: See [CLAUDE.md](CLAUDE.md) for contributing

---

**Happy Learning! 🎓**
