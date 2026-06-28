import torch

from explainability.services.explainability_service import (
    ExplainabilityService
)

service = (
    ExplainabilityService()
)

image = (
    torch.randn(
        1,
        3,
        224,
        224
    )
)

result = (
    service.analyze(
        image_tensor=image,
        prediction="PNEUMONIA",
        confidence=96.8
    )
)

print(result)