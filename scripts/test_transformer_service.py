import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import torch

from ai_engine.transformer_engine.transformer_service import TransformerService


service = TransformerService()

x = torch.randint(
    0,
    1000,
    (2, 16)
)

embeddings = service.generate_embeddings(x)

print("Embedding Shape:")
print(embeddings.shape)

print()

print("Model Summary:")
print(service.model_summary())