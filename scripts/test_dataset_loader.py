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

from models.train_xray_model import (
    ChestXRayDataLoader
)

loader_builder = (
    ChestXRayDataLoader()
)

train_loader, train_dataset = (
    loader_builder.get_train_loader()
)

print("\nDATASET INFO")
print("=" * 50)

print(
    "Classes:",
    train_dataset.classes
)

print(
    "Total Images:",
    len(train_dataset)
)

images, labels = next(
    iter(train_loader)
)

print(
    "Batch Shape:",
    images.shape
)

print(
    "Labels Shape:",
    labels.shape
)