import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))

from rag.embeddings.sentence_transformer_embedder import (
    SentenceTransformerEmbedder
)

from vector_store.faiss_store import FAISSStore


embedder = SentenceTransformerEmbedder()

store = FAISSStore()


documents = [
    "Pneumonia causes fever and cough.",
    "Diabetes affects blood sugar levels.",
    "Hypertension is high blood pressure."
]

embeddings = embedder.embed_documents(
    documents
)

store.add_documents(
    documents,
    embeddings
)

query_embedding = embedder.embed_text(
    "What causes fever?"
)

results = store.search(
    query_embedding,
    top_k=2
)

print("\nRetrieved Documents")
print("=" * 50)

for doc in results:
    print(doc)
    