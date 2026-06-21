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

from ai_engine.gemini_engine.medical_explainer import (
    MedicalExplainer
)

explainer = (
    MedicalExplainer()
)

result = (
    explainer.explain(
        prediction="NORMAL",
        confidence=99.4
    )
)

print(
    "\nMEDICAL EXPLANATION"
)

print("=" * 60)

print(result)