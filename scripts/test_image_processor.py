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

from multimodal.image_processor import (
    ImageProcessor
)

processor = ImageProcessor()

image_path = (
    "datasets/chest_xray/test/NORMAL/"
)

import os

first_image = os.listdir(
    image_path
)[0]

full_path = os.path.join(
    image_path,
    first_image
)

tensor = processor.preprocess(
    full_path
)

print(
    "\nIMAGE TENSOR SHAPE"
)

print(
    "=" * 50
)

print(
    tensor.shape
)