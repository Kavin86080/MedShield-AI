import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_engine.prompt_engine.prompt_service import PromptService


service = PromptService()

prompt1 = service.generate_prompt(
    template_name="zero_shot",
    question="What is pneumonia?"
)

prompt2 = service.generate_prompt(
    template_name="medical_qa",
    context="Patient has chest pain.",
    question="Possible causes?"
)

print("Generated Prompt")
print("=" * 50)
print(prompt1)

print()

print("Prompt Statistics")
print("=" * 50)
print(
    service.prompt_statistics()
)

print()

print("Prompt History")
print("=" * 50)
print(
    service.get_prompt_history()
)