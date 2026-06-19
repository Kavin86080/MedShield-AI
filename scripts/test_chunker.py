import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rag.loaders.text_loader import TextLoader
from rag.chunkers.recursive_chunker import RecursiveChunker


loader = TextLoader()

text = loader.load(
    "datasets/raw/sample_medical.txt"
)

chunker = RecursiveChunker(
    chunk_size=50,
    overlap=10
)

chunks = chunker.chunk_text(text)

print("Generated Chunks")
print("=" * 50)

for i, chunk in enumerate(chunks):

    print(f"\nChunk {i+1}")
    print("-" * 30)
    print(chunk)