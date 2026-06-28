# Placeholder for evaluate_model.py
import os
import sys

sys.path.append(
    os.path.abspath(
        os.path.join(
            os.path.dirname(__file__),
            ".."
        )
    )
)

import torch
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

from torchvision.datasets import ImageFolder
from torchvision import transforms
from torch.utils.data import DataLoader

from models.chest_xray_model import (
    ChestXRayModel
)

# ----------------------------------
# Device
# ----------------------------------

device = (
    "cuda"
    if torch.cuda.is_available()
    else "cpu"
)

# ----------------------------------
# Transform
# ----------------------------------

transform = transforms.Compose([

    transforms.Resize(
        (224, 224)
    ),

    transforms.ToTensor(),

    transforms.Normalize(
        mean=[
            0.485,
            0.456,
            0.406
        ],

        std=[
            0.229,
            0.224,
            0.225
        ]
    )
])

# ----------------------------------
# Dataset
# ----------------------------------

dataset = ImageFolder(
    "datasets/chest_xray/test",
    transform=transform
)

loader = DataLoader(
    dataset,
    batch_size=32,
    shuffle=False
)

# ----------------------------------
# Model
# ----------------------------------

model = ChestXRayModel()

model.load_state_dict(
    torch.load(
        "models/chest_xray_model.pth",
        map_location=device
    )
)

model.to(device)
model.eval()

# ----------------------------------
# Evaluation
# ----------------------------------

y_true = []
y_pred = []

with torch.no_grad():

    for images, labels in loader:

        images = images.to(device)

        outputs = model(images)

        preds = outputs.argmax(
            dim=1
        )

        y_true.extend(
            labels.cpu().numpy()
        )

        y_pred.extend(
            preds.cpu().numpy()
        )

# ----------------------------------
# Metrics
# ----------------------------------

accuracy = accuracy_score(
    y_true,
    y_pred
)

precision = precision_score(
    y_true,
    y_pred
)

recall = recall_score(
    y_true,
    y_pred
)

f1 = f1_score(
    y_true,
    y_pred
)

print("\nMODEL EVALUATION")
print("=" * 60)

print(
    f"Accuracy  : {accuracy:.4f}"
)

print(
    f"Precision : {precision:.4f}"
)

print(
    f"Recall    : {recall:.4f}"
)

print(
    f"F1 Score  : {f1:.4f}"
)

print("\nCONFUSION MATRIX")
print(
    confusion_matrix(
        y_true,
        y_pred
    )
)

print("\nCLASSIFICATION REPORT")
print(
    classification_report(
        y_true,
        y_pred,
        target_names=[
            "NORMAL",
            "PNEUMONIA"
        ]
    )
)