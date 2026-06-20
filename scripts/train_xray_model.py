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
import torch.nn as nn

from models.chest_xray_model import (
    ChestXRayModel
)

from models.train_xray_model import (
    ChestXRayDataLoader
)

# --------------------------
# Device
# --------------------------

device = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

print(
    f"\nUsing Device: {device}"
)

# --------------------------
# Dataset
# --------------------------

loader_builder = (
    ChestXRayDataLoader()
)

train_loader, train_dataset = (
    loader_builder.get_train_loader(
        batch_size=16
    )
)

# --------------------------
# Model
# --------------------------

model = (
    ChestXRayModel()
).to(device)

# --------------------------
# Loss Function
# --------------------------

criterion = (
    nn.CrossEntropyLoss()
)

# --------------------------
# Optimizer
# --------------------------

optimizer = (
    torch.optim.Adam(
        model.parameters(),
        lr=0.0001
    )
)

# --------------------------
# Training
# --------------------------

epochs = 3

for epoch in range(
    epochs
):

    model.train()

    running_loss = 0.0

    for images, labels in train_loader:

        images = images.to(
            device
        )

        labels = labels.to(
            device
        )

        optimizer.zero_grad()

        outputs = model(
            images
        )

        loss = criterion(
            outputs,
            labels
        )

        loss.backward()

        optimizer.step()

        running_loss += (
            loss.item()
        )

    print(
        f"Epoch {epoch+1}/{epochs}"
        f" | Loss: "
        f"{running_loss:.4f}"
    )

# --------------------------
# Save Model
# --------------------------

torch.save(
    model.state_dict(),
    "models/chest_xray_model.pth"
)

print(
    "\nModel Saved Successfully"
)