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

from models.inference_xray import (
    XRayInference
)

predictor = (
    XRayInference(
        model_path=
        "models/chest_xray_model.pth"
    )
)

result = predictor.predict(

    "datasets/chest_xray/test/NORMAL/"
    + __import__("os").listdir(
        "datasets/chest_xray/test/NORMAL"
    )[0]
)

print(
    "\nPREDICTION"
)

print("=" * 50)

print(result)