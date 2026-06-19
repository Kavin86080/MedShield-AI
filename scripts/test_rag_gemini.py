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

from dotenv import load_dotenv

load_dotenv()

from rag.pipelines.rag_gemini_pipeline import (
    RAGGeminiPipeline
)


pipeline = RAGGeminiPipeline()

documents = [

    """
    Pneumonia is a lung infection that causes
    fever, cough and breathing difficulty.
    """,

    """
    Diabetes is a chronic disease affecting
    blood glucose regulation.
    """,

    """
    Hypertension is persistent high blood pressure.
    """,

    """
    Asthma causes inflammation of airways.
    """
]

pipeline.index_documents(
    documents
)

result = pipeline.ask(
    question="What disease causes fever?"
)

print("\nQUESTION")
print("=" * 60)
print(result["question"])

print("\nANSWER")
print("=" * 60)
print(result["answer"])