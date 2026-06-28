import torch

from explainability.explanation_report import (
    ExplanationReport
)

dummy_model = None

report_engine = (
    ExplanationReport(
        dummy_model
    )
)

dummy_image = (
    torch.randn(
        1,
        3,
        224,
        224
    )
)

report = (
    report_engine.generate(
        image_tensor=dummy_image,
        prediction="PNEUMONIA",
        confidence=94.3
    )
)

print(report)