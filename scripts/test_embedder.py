import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rag.embeddings.sentence_transformer_embedder import (
    SentenceTransformerEmbedder
)

embedder = SentenceTransformerEmbedder()

embedding = embedder.embed_text(
    "Pneumonia causes fever and cough."
)

print("Embedding Length:")
print(len(embedding))

print()

print("First 10 Values:")
print(embedding[:10])