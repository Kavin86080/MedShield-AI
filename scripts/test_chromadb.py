import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rag.embeddings.sentence_transformer_embedder import (
    SentenceTransformerEmbedder
)

from vector_store.chroma_store import ChromaStore


embedder = SentenceTransformerEmbedder()

store = ChromaStore()


documents = [
    "Pneumonia causes fever and cough.",
    "Diabetes affects blood sugar levels.",
    "Hypertension is high blood pressure."
]

embeddings = embedder.embed_documents(
    documents
)

store.add_documents(
    ids=["1", "2", "3"],
    documents=documents,
    embeddings=embeddings
)

query_embedding = embedder.embed_text(
    "What causes fever?"
)

results = store.query(
    query_embedding
)

print(results["documents"][0])