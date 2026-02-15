#!/usr/bin/env python3
"""
Standalone PDF converter - Convert existing Markdown notes to PDF

Usage:
    python scripts/standalone_pdf_converter.py notes.md
    python scripts/standalone_pdf_converter.py notes.md -o output.pdf
    python scripts/standalone_pdf_converter.py input_dir/ --batch
"""

import sys
import argparse
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from pdf_generator import PDFGenerator

def main():
    parser = argparse.ArgumentParser(
        description='Convert Markdown notes to tablet-friendly PDF'
    )
    parser.add_argument(
        'input',
        help='Input Markdown file or directory'
    )
    parser.add_argument(
        '-o', '--output',
        help='Output PDF path (auto-generated if not specified)'
    )
    parser.add_argument(
        '--batch',
        action='store_true',
        help='Batch convert all .md files in directory'
    )

    args = parser.parse_args()

    input_path = Path(args.input)
    generator = PDFGenerator()

    if args.batch:
        if not input_path.is_dir():
            print(f"Error: {input_path} is not a directory")
            sys.exit(1)

        md_files = list(input_path.glob('*.md'))
        if not md_files:
            print(f"No .md files found in {input_path}")
            sys.exit(1)

        print(f"Converting {len(md_files)} Markdown files to PDF...\n")

        for md_file in md_files:
            print(f"Converting: {md_file.name}")
            pdf_path = generator.generate_pdf(md_file)
            if pdf_path:
                print(f"  ✓ Saved: {pdf_path.name}\n")
            else:
                print(f"  ✗ Failed\n")

    else:
        if not input_path.exists():
            print(f"Error: {input_path} not found")
            sys.exit(1)

        output_path = Path(args.output) if args.output else None

        print(f"Converting {input_path.name} to PDF...")
        pdf_path = generator.generate_pdf(input_path, output_path)

        if pdf_path:
            print(f"✓ PDF saved: {pdf_path}")
        else:
            print("✗ PDF generation failed")
            sys.exit(1)

if __name__ == '__main__':
    main()
