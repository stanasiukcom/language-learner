# 🚀 Quick Start Guide

Get started with Language Learner in 5 minutes.

---

## Step 1: Install Dependencies

### macOS
```bash
# Install system dependencies
brew install ffmpeg poppler yt-dlp pango gdk-pixbuf glib

# Install Python packages
pip install -r requirements.txt
```

### Linux (Ubuntu/Debian)
```bash
# Install system dependencies
sudo apt-get update
sudo apt-get install ffmpeg poppler-utils python3-pip \
  python3-cffi python3-brotli libpango-1.0-0 libgdk-pixbuf2.0-0

# Install yt-dlp
pip install yt-dlp

# Install Python packages
pip install -r requirements.txt
```

### Windows
```bash
# Install via Chocolatey
choco install ffmpeg

# Install Python packages
pip install -r requirements.txt
pip install yt-dlp
```

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
python src/main.py
```

This will:
1. ⬇️  Download all videos
2. 🎙️  Extract audio and transcribe
3. 📝  Generate comprehensive study notes

### Step-by-Step (Optional)
```bash
# Download only
python src/main.py --download-only

# Transcribe only
python src/main.py --transcribe-only

# Generate notes only
python src/main.py --notes-only

# Use custom config file
python src/main.py -c config/my_config.yaml
```

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
```bash
pip install yt-dlp
```

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
