import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from rag.loaders.text_loader import TextLoader


loader = TextLoader()

content = loader.load(
    "datasets/raw/sample_medical.txt"
)

print("Document Content")
print("=" * 50)
print(content)