import os

from models.inference_xray import (
    XRayInference
)

model = XRayInference(
    "models/chest_xray_model.pth"
)

test_images = [

    "datasets/chest_xray/test/NORMAL",

    "datasets/chest_xray/test/PNEUMONIA"

]

print("\nMODEL PREDICTION TEST")
print("=" * 60)

for folder in test_images:

    files = os.listdir(folder)[:5]

    print(f"\nFolder: {folder}")

    for file in files:

        image_path = os.path.join(
            folder,
            file
        )

        result = model.predict(
            image_path
        )

        print(
            file,
            "->",
            result
        ) 