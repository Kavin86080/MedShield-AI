import sys
import os

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

from multimodal.gradcam_processor import (
    GradCAMProcessor
)

processor = (
    GradCAMProcessor(
        model_path=
        "models/chest_xray_model.pth"
    )
)

image_folder = (
    "datasets/chest_xray/test/NORMAL"
)

image_file = os.listdir(
    image_folder
)[0]

image_path = os.path.join(
    image_folder,
    image_file
)

result = (
    processor.generate_heatmap(
        image_path
    )
)

print(
    "\nGRADCAM SAVED"
)

print("=" * 50)

print(result)