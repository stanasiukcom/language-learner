#!/usr/bin/env python3
"""
Generate tablet-friendly PDF files from Markdown notes
"""

import markdown
from pathlib import Path
from typing import Optional
import logging

logger = logging.getLogger(__name__)

class PDFGenerator:
    """Generate tablet-friendly PDFs from Markdown"""

    # Tablet-friendly CSS styling
    PDF_STYLES = """
    <style>
        @page {
            size: A4;
            margin: 2cm 1.5cm;
            @top-center {
                content: "Language Learning Notes";
                font-size: 10pt;
                color: #666;
            }
            @bottom-center {
                content: counter(page);
                font-size: 10pt;
                color: #666;
            }
        }

        body {
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.6;
            color: #333;
            max-width: 100%;
        }

        h1 {
            font-size: 24pt;
            font-weight: bold;
            color: #1a1a1a;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            page-break-after: avoid;
            border-bottom: 2px solid #4A90E2;
            padding-bottom: 0.3em;
        }

        h2 {
            font-size: 18pt;
            font-weight: bold;
            color: #2c3e50;
            margin-top: 1.3em;
            margin-bottom: 0.4em;
            page-break-after: avoid;
        }

        h3 {
            font-size: 14pt;
            font-weight: bold;
            color: #34495e;
            margin-top: 1em;
            margin-bottom: 0.3em;
            page-break-after: avoid;
        }

        h4 {
            font-size: 12pt;
            font-weight: bold;
            color: #555;
            margin-top: 0.8em;
            margin-bottom: 0.3em;
        }

        p {
            margin: 0.5em 0;
            text-align: justify;
        }

        /* Table styling */
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 1em 0;
            font-size: 10pt;
            page-break-inside: avoid;
        }

        th {
            background-color: #4A90E2;
            color: white;
            padding: 10px;
            text-align: left;
            font-weight: bold;
        }

        td {
            padding: 8px 10px;
            border: 1px solid #ddd;
        }

        tr:nth-child(even) {
            background-color: #f9f9f9;
        }

        /* Code and preformatted text */
        code {
            background-color: #f4f4f4;
            padding: 2px 6px;
            border-radius: 3px;
            font-family: "SF Mono", Monaco, "Courier New", monospace;
            font-size: 10pt;
            color: #c7254e;
        }

        pre {
            background-color: #f4f4f4;
            padding: 12px;
            border-radius: 5px;
            border-left: 4px solid #4A90E2;
            overflow-x: auto;
            font-size: 9pt;
            line-height: 1.4;
            page-break-inside: avoid;
        }

        pre code {
            background: none;
            padding: 0;
            color: inherit;
        }

        /* Lists */
        ul, ol {
            margin: 0.5em 0;
            padding-left: 2em;
        }

        li {
            margin: 0.3em 0;
        }

        /* Blockquotes */
        blockquote {
            border-left: 4px solid #4A90E2;
            padding-left: 1em;
            margin: 1em 0;
            color: #555;
            font-style: italic;
            background-color: #f9f9f9;
            padding: 0.5em 1em;
        }

        /* Links */
        a {
            color: #4A90E2;
            text-decoration: none;
        }

        a:hover {
            text-decoration: underline;
        }

        /* Horizontal rules */
        hr {
            border: none;
            border-top: 2px solid #ddd;
            margin: 2em 0;
        }

        /* Emoji and icons - ensure proper display */
        .emoji {
            font-family: "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif;
        }

        /* Timestamps */
        strong {
            color: #2c3e50;
        }

        /* Checklist items */
        input[type="checkbox"] {
            margin-right: 0.5em;
        }

        /* Table of contents */
        nav ul {
            list-style-type: none;
            padding-left: 0;
        }

        nav a {
            color: #4A90E2;
            text-decoration: none;
        }

        /* Page breaks */
        .page-break {
            page-break-before: always;
        }

        /* Avoid breaking these elements */
        .no-break {
            page-break-inside: avoid;
        }

        /* RTL support for Arabic, Hebrew, etc. */
        [dir="rtl"] {
            direction: rtl;
            text-align: right;
        }

        /* Print-friendly adjustments */
        @media print {
            body {
                font-size: 10pt;
            }
            h1 { font-size: 20pt; }
            h2 { font-size: 16pt; }
            h3 { font-size: 13pt; }
        }
    </style>
    """

    def __init__(self, tablet_mode: str = "standard"):
        """
        Initialize PDF generator

        Args:
            tablet_mode: "standard" (A4), "tablet" (smaller margins), or "ebook" (compact)
        """
        self.tablet_mode = tablet_mode

        # Set up library path for macOS (for WeasyPrint dependencies)
        self._setup_library_path()

        # Check if weasyprint is available
        try:
            from weasyprint import HTML, CSS
            self.weasyprint_available = True
            self.HTML = HTML
            self.CSS = CSS
        except ImportError:
            logger.warning("weasyprint not installed. PDF generation will be unavailable.")
            logger.info("Install with: pip install weasyprint && brew install pango gdk-pixbuf glib")
            self.weasyprint_available = False
        except OSError as e:
            if "gobject" in str(e).lower():
                logger.warning("WeasyPrint system dependencies not found.")
                logger.info("Install with: brew install pango gdk-pixbuf glib gobject-introspection")
                logger.info("Or set: export DYLD_LIBRARY_PATH=/opt/homebrew/lib:$DYLD_LIBRARY_PATH")
            else:
                logger.warning(f"WeasyPrint initialization error: {e}")
            self.weasyprint_available = False

    def _setup_library_path(self):
        """Set up library path for macOS"""
        import os
        import platform

        if platform.system() == "Darwin":  # macOS
            homebrew_lib = "/opt/homebrew/lib"
            if os.path.exists(homebrew_lib):
                current_path = os.environ.get("DYLD_LIBRARY_PATH", "")
                if homebrew_lib not in current_path:
                    os.environ["DYLD_LIBRARY_PATH"] = f"{homebrew_lib}:{current_path}"

    def markdown_to_html(self, markdown_path: Path) -> str:
        """
        Convert Markdown file to HTML with styling

        Args:
            markdown_path: Path to Markdown file

        Returns:
            HTML string with embedded CSS
        """
        # Read Markdown content
        with open(markdown_path, 'r', encoding='utf-8') as f:
            md_content = f.read()

        # Convert Markdown to HTML with extensions
        html_content = markdown.markdown(
            md_content,
            extensions=[
                'extra',          # Tables, fenced code, etc.
                'codehilite',     # Syntax highlighting
                'toc',            # Table of contents
                'sane_lists',     # Better list handling
                'nl2br',          # Newline to <br>
            ]
        )

        # Wrap in full HTML document with styling
        full_html = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Language Learning Notes</title>
    {self.PDF_STYLES}
</head>
<body>
    {html_content}
</body>
</html>
"""
        return full_html

    def generate_pdf(self, markdown_path: Path, pdf_path: Optional[Path] = None) -> Optional[Path]:
        """
        Generate PDF from Markdown file

        Args:
            markdown_path: Path to input Markdown file
            pdf_path: Optional output PDF path (auto-generated if None)

        Returns:
            Path to generated PDF file, or None if failed
        """
        if not self.weasyprint_available:
            logger.error("Cannot generate PDF: weasyprint not installed")
            logger.info("Install with: pip install weasyprint")
            return None

        # Auto-generate PDF path if not provided
        if pdf_path is None:
            pdf_path = markdown_path.with_suffix('.pdf')

        try:
            logger.info(f"Converting {markdown_path.name} to PDF...")

            # Convert Markdown to HTML
            html_content = self.markdown_to_html(markdown_path)

            # Generate PDF from HTML
            from weasyprint import HTML
            html_doc = HTML(string=html_content)
            html_doc.write_pdf(str(pdf_path))

            # Get file size for logging
            size_mb = pdf_path.stat().st_size / (1024 * 1024)
            logger.info(f"✓ PDF generated: {pdf_path.name} ({size_mb:.2f} MB)")

            return pdf_path

        except Exception as e:
            logger.error(f"PDF generation failed: {e}")
            return None

    def generate_from_notes(self, notes_path: Path, output_dir: Optional[Path] = None) -> Optional[Path]:
        """
        Generate PDF from comprehensive notes

        Args:
            notes_path: Path to Markdown notes file
            output_dir: Optional output directory (same as notes if None)

        Returns:
            Path to generated PDF, or None if failed
        """
        if output_dir:
            pdf_path = output_dir / notes_path.with_suffix('.pdf').name
        else:
            pdf_path = notes_path.with_suffix('.pdf')

        return self.generate_pdf(notes_path, pdf_path)


def generate_pdf_from_markdown(markdown_path: Path, pdf_path: Optional[Path] = None) -> Optional[Path]:
    """
    Convenience function to generate PDF from Markdown

    Args:
        markdown_path: Path to Markdown file
        pdf_path: Optional output PDF path

    Returns:
        Path to generated PDF, or None if failed
    """
    generator = PDFGenerator()
    return generator.generate_pdf(markdown_path, pdf_path)
