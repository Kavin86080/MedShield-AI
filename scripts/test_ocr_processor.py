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

from multimodal.ocr_processor import OCRProcessor

ocr = OCRProcessor()

text = ocr.extract_text(
    "datasets/images/CBC_REPORT.webp"
)

print("\nOCR TEXT")
print("=" * 60)

print(text)