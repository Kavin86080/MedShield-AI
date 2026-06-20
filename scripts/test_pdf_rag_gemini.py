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

from rag.pipelines.pdf_rag_gemini_pipeline import (
    PDFRAGGeminiPipeline
)

pipeline = (
    PDFRAGGeminiPipeline()
)

pipeline.index_pdf(
    "datasets/reports/medisense_paper.pdf"
)

result = pipeline.ask(
    "What is MediSense?"
)

print("\nQUESTION")
print("=" * 60)

print(
    result["question"]
)

print("\nANSWER")
print("=" * 60)

print(
    result["answer"]
)