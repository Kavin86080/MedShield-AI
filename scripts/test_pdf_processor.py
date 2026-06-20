import sys
from pathlib import Path

PROJECT_ROOT = (
    Path(__file__)
    .resolve()
    .parent.parent
)

sys.path.insert(
    0,
    str(PROJECT_ROOT)
)

from multimodal.pdf_processor import (
    PDFProcessor
)

processor = PDFProcessor()

pdf_file = (
    "datasets/reports/medisense_paper.pdf"
)

text = processor.extract_text(
    pdf_file
)

print("\nPDF CONTENT")
print("=" * 60)

print(
    text[:1000]
)

print("\nPAGE COUNT")
print("=" * 60)

print(
    processor.get_page_count(
        pdf_file
    )
)