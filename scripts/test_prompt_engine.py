import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_engine.prompt_engine.prompt_engine import PromptEngine


engine = PromptEngine()

print("Available Templates")
print("=" * 50)

print(
    engine.get_available_templates()
)

print()

prompt = engine.build_prompt(
    template_name="medical_qa",
    context="Patient has fever, cough and fatigue.",
    question="Possible diagnosis?"
)

print("Generated Prompt")
print("=" * 50)

print(prompt)