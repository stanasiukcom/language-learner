# 📱 PDF Generation Guide

Language Learner automatically generates tablet-friendly PDF versions of your study notes alongside the Markdown files.

---

## ✨ Features

- **Tablet-Optimized Layout** - Perfect for reading on iPad, Android tablets, or e-readers
- **Beautiful Typography** - Clean, readable fonts with proper spacing
- **Professional Styling**:
  - Color-coded headers with visual hierarchy
  - Syntax-highlighted code blocks
  - Clean, organized tables
  - Proper page breaks to avoid splitting content
  - Embedded timestamps as clickable links

- **Multi-Language Support**:
  - RTL support for Arabic, Hebrew, Farsi
  - Proper rendering of CJK characters (Chinese, Japanese, Korean)
  - Unicode emoji and special characters

- **Print-Ready** - A4 format with proper margins

---

## 🚀 Quick Start

PDFs are generated automatically when you run the main processing:

```bash
python src/main.py
```

Output:
```
output/
├── Comprehensive_Notes_Arabic_AR1.md   # Markdown version
└── Comprehensive_Notes_Arabic_AR1.pdf  # PDF version (tablet-friendly)
```

---

## ⚙️ Configuration

### Enable/Disable PDF Generation

Edit your `config/config.yaml`:

```yaml
notes:
  generate_pdf: true  # Set to false to skip PDF generation
```

### PDF Styling

The PDF generator uses responsive styling that adapts to:
- **Tablet screens** - Optimized for 9-12" displays
- **Print** - A4 paper with appropriate margins
- **E-readers** - Compatible with most PDF readers

---

## 🔧 Installation

### macOS

```bash
# Install system dependencies
brew install pango gdk-pixbuf glib gobject-introspection

# Install Python packages
pip install markdown weasyprint
```

### Linux (Ubuntu/Debian)

```bash
# Install system dependencies
sudo apt-get install \
  python3-cffi \
  python3-brotli \
  libpango-1.0-0 \
  libharfbuzz0b \
  libpangoft2-1.0-0 \
  libgdk-pixbuf2.0-0

# Install Python packages
pip install markdown weasyprint
```

### Windows

```bash
# Install GTK3 runtime
# Download from: https://github.com/tschoonj/GTK-for-Windows-Runtime-Environment-Installer

# Install Python packages
pip install markdown weasyprint
```

---

## 📝 Standalone Converter

Convert existing Markdown notes to PDF without re-running the entire pipeline:

### Single File

```bash
python scripts/standalone_pdf_converter.py notes.md
# Creates: notes.pdf
```

### Custom Output

```bash
python scripts/standalone_pdf_converter.py notes.md -o my_study_guide.pdf
```

### Batch Conversion

```bash
python scripts/standalone_pdf_converter.py output/ --batch
# Converts all .md files in output/ directory
```

---

## 🎨 Customization

### Modify PDF Styling

Edit `src/pdf_generator.py` - look for the `PDF_STYLES` constant:

```python
PDF_STYLES = """
<style>
    /* Customize colors, fonts, spacing here */
    h1 {
        color: #1a1a1a;
        font-size: 24pt;
    }

    /* Add your custom CSS */
</style>
"""
```

### Custom Page Size

For different tablet sizes:

```python
@page {
    size: letter;  # or A4, A5, etc.
    margin: 2cm;
}
```

---

## 🐛 Troubleshooting

### "WeasyPrint not installed"

```bash
pip install weasyprint
```

### "Cannot load library 'libgobject-2.0-0'" (macOS)

```bash
# Install missing system libraries
brew install pango gdk-pixbuf glib gobject-introspection

# Set library path (add to ~/.zshrc or ~/.bash_profile)
export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH
```

### "Library not found" (Linux)

```bash
sudo apt-get install libpango-1.0-0 libgdk-pixbuf2.0-0
```

### PDF is blank or has rendering issues

- Ensure all system dependencies are installed
- Check that fonts are available on your system
- Try regenerating with: `python scripts/standalone_pdf_converter.py notes.md`

### Large PDF file size

The PDF includes embedded fonts for consistency. Typical sizes:
- Small course (3-5 lessons): 300-500 KB
- Medium course (10-15 lessons): 1-2 MB
- Large course (30+ lessons): 3-5 MB

---

## 📚 Advanced Usage

### Programmatic PDF Generation

```python
from pdf_generator import PDFGenerator

generator = PDFGenerator()
pdf_path = generator.generate_pdf(
    markdown_path='notes.md',
    pdf_path='output.pdf'
)
```

### Generate from String

```python
from pdf_generator import PDFGenerator

generator = PDFGenerator()
html_content = generator.markdown_to_html(markdown_path)
# Modify HTML as needed
generator.HTML(string=html_content).write_pdf('custom.pdf')
```

---

## 💡 Tips

1. **Preview before sharing** - Open PDFs on different devices to check rendering
2. **Optimize for target device** - Consider screen size of your primary study device
3. **Use PDF bookmarks** - Most PDF readers support navigation via table of contents
4. **Annotate on tablet** - Use apps like GoodNotes, Notability, or PDF Expert for annotations
5. **Sync across devices** - Store PDFs in cloud storage (Dropbox, iCloud, Google Drive)

---

## 🎯 Best Practices

### For Students
- Download PDFs to tablet for offline study
- Use split-screen: PDF notes + flashcard app
- Annotate directly on PDF during review

### For Teachers
- Share PDFs with students via LMS or email
- Include QR codes linking to video timestamps
- Print PDFs for in-class reference

### For Self-Learners
- Read PDFs on commute or during travel
- Use PDF highlighting to mark vocabulary
- Export annotations back to Anki/Notion

---

## 📖 Examples

See `examples/` directory for sample PDF outputs from various languages:
- `arabic_notes_sample.pdf` - Arabic with RTL support
- `japanese_notes_sample.pdf` - Kanji rendering
- `spanish_notes_sample.pdf` - Standard Latin script

---

**Questions? Issues?**

- 🐛 Report bugs: [GitHub Issues](https://github.com/stanasiukcom/language-learner/issues)
- 💬 Discuss: [GitHub Discussions](https://github.com/stanasiukcom/language-learner/discussions)
