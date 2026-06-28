from explainability.metrics.explanation_score import (
    ExplanationScore
)

score = (
    ExplanationScore.calculate(
        confidence=96.8,
        shap_importance=0.92
    )
)

print(
    f"Explainability Score: {score}"
)