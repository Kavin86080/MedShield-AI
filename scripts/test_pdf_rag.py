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

from rag.pipelines.pdf_rag_pipeline import (
    PDFRAGPipeline
)

pipeline = PDFRAGPipeline()

chunk_count = (
    pipeline.index_pdf(
        "datasets/reports/medisense_paper.pdf"
    )
)

print(
    "\nTOTAL CHUNKS"
)

print(
    "=" * 60
)

print(
    chunk_count
)

results = (
    pipeline.query(
        "What is MediSense?"
    )
)

print(
    "\nRETRIEVED CONTEXT"
)

print(
    "=" * 60
)

for i, chunk in enumerate(
    results,
    start=1
):

    print(
        f"\nChunk {i}"
    )

    print(
        "-" * 30
    )

    print(
        chunk
    )