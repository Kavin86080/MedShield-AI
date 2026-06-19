import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_engine.prompt_engine.prompt_templates import (
    ZERO_SHOT_TEMPLATE,
    FEW_SHOT_TEMPLATE,
    CHAIN_OF_THOUGHT_TEMPLATE,
    REACT_TEMPLATE
)

print("ZERO SHOT")
print("=" * 50)
print(
    ZERO_SHOT_TEMPLATE.format(
        question="What is pneumonia?"
    )
)

print()

print("FEW SHOT")
print("=" * 50)
print(
    FEW_SHOT_TEMPLATE.format(
        question="What is asthma?"
    )
)

print()

print("CHAIN OF THOUGHT")
print("=" * 50)
print(
    CHAIN_OF_THOUGHT_TEMPLATE.format(
        question="Why does fever occur?"
    )
)

print()

print("REACT")
print("=" * 50)
print(
    REACT_TEMPLATE.format(
        question="What are symptoms of tuberculosis?"
    )
)