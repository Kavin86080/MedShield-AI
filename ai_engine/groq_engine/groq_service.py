from ai_engine.groq_engine.groq_client import (
    GroqClient
)


class GroqService:

    def __init__(self):

        self.client = (
            GroqClient()
        )

    def ask(
        self,
        prompt
    ):

        return (
            self.client.generate(
                prompt
            )
        )

    def generate_medical_summary(
        self,
        question,
        context
    ):

        prompt = f"""
You are MedShield-X Clinical AI Assistant.

Use ONLY the provided medical evidence.

Question:
{question}

Medical Evidence:
{context}

Instructions:

1. Answer directly.
2. Summarize clinically.
3. Mention symptoms if available.
4. Mention treatment if available.
5. Mention risk factors if available.
6. Mention important warnings.
7. Do not invent information.
8. Use bullet points.

Output Format:

Medical Summary:
...

Key Findings:
• ...
• ...

Clinical Notes:
• ...
• ...

References:
...
"""

        return self.ask(
            prompt
        )