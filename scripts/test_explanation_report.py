import torch

from explainability.gradcam_explainer import (
    CAMExplainer
)

from explainability.shap_explainer import (
    SHAPExplainer
)

from explainability.explanation_report import (
    ExplanationReport
)

from models.chest_xray_model import (
    ChestXRayModel
)


# Load model

model = ChestXRayModel()

# DenseNet121 target layer

target_layer = (
    model.model.features.denseblock4
)

# Initialize explainers

cam_explainer = (
    CAMExplainer(
        model=model,
        target_layer=target_layer
    )
)

shap_explainer = (
    SHAPExplainer(
        model=model
    )
)

# Report engine

report_engine = (
    ExplanationReport(
        cam_explainer=cam_explainer,
        shap_explainer=shap_explainer
    )
)

# Dummy image

image_tensor = (
    torch.randn(
        1,
        3,
        224,
        224
    )
)

# Generate report

report = (
    report_engine.generate_report(
        image_tensor=image_tensor,
        prediction="PNEUMONIA",
        confidence=96.8
    )
)

print("\nREPORT GENERATED\n")

print(
    "Prediction:",
    report["prediction"]
)

print(
    "Confidence:",
    report["confidence"]
)

print(
    "SHAP:",
    report["shap"]
)

print(
    "Clinical Explanation:"
)

print(
    report["clinical_explanation"]
)

print(
    "\nGradCAM Shape:",
    report["gradcam"].shape
)

print(
    "ScoreCAM Shape:",
    report["scorecam"].shape
)

print(
    "EigenCAM Shape:",
    report["eigencam"].shape
)

print(
    "LayerCAM Shape:",
    report["layercam"].shape
)