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

import torch

from models.chest_xray_model import (
    ChestXRayModel
)

model = ChestXRayModel()

dummy = torch.randn(
    1,
    3,
    224,
    224
)

output = model(
    dummy
)

print(
    "\nMODEL OUTPUT SHAPE"
)

print("=" * 50)

print(
    output.shape
)