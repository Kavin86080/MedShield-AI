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

from dotenv import load_dotenv

load_dotenv()

from ai_engine.gemini_engine.gemini_service import (
    GeminiService
)

service = GeminiService()

response = service.ask(
    "What is pneumonia?"
)

print("\nGemini Response")
print("=" * 50)

print(response)