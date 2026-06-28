from ai_engine.groq_engine.groq_service import (
    GroqService
)

service = (
    GroqService()
)

response = service.ask(
    "What is pneumonia?"
)

print(response)