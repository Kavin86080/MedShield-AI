import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

import torch

from ai_engine.transformer_engine.transformer_engine import MiniTransformer

model = MiniTransformer()

x = torch.randint(
    0,
    1000,
    (2, 16)
)

output = model(x)

print("Output Shape:", output.shape)