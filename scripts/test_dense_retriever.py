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

from rag.retrievers.dense_retriever import (
    DenseRetriever
)


retriever = DenseRetriever()

documents = [

    "Pneumonia is an infection that causes fever and cough.",

    "Diabetes affects blood glucose regulation.",

    "Hypertension is high blood pressure.",

    "Asthma causes airway inflammation."
]

retriever.index_documents(
    documents
)

results = retriever.retrieve(
    query="What disease causes fever?",
    top_k=2
)

print("\nRetrieved Documents")
print("=" * 50)

for doc in results:
    print(doc)

print("\nTotal Documents")
print("=" * 50)

print(
    retriever.total_documents()
)