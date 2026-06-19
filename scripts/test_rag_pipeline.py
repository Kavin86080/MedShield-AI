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

from rag.pipelines.rag_pipeline import (
    RAGPipeline
)

pipeline = RAGPipeline()

documents = [

    "Pneumonia is a lung infection that causes fever and cough.",

    "Diabetes is a metabolic disease affecting blood sugar.",

    "Hypertension is persistent high blood pressure.",

    "Asthma causes inflammation of airways."
]

pipeline.index_documents(
    documents
)

result = pipeline.query(
    "What disease causes fever?"
)

print("\nGenerated RAG Prompt")
print("=" * 60)

print(
    result["prompt"]
)