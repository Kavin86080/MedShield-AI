import torch

from explainability.shap_explainer import (
    SHAPExplainer
)

dummy_model = None

explainer = (
    SHAPExplainer(
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

result = (
    explainer.explain(
        dummy_image
    )
)

print(result)