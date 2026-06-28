from ai_engine.gemini_engine.gemini_client import (
    GeminiClient
)


class GeminiService:

    def __init__(self):

        self.client = (
            GeminiClient()
        )

    def ask(
        self,
        prompt: str
    ) -> str:

        return (
            self.client.generate(
                prompt
            )
        )

    def generate_clinical_summary(
        self,
        question,
        context
    ):

        prompt = f"""
You are an expert Clinical AI Assistant.

Question:
{question}

Medical Evidence:
{context}

Instructions:

1. Answer the question directly.
2. Use only the provided evidence.
3. Summarize clinically.
4. Mention symptoms if available.
5. Mention treatment if available.
6. Mention important warnings.
7. Cite source type.

Format:

Medical Summary:
...

Key Findings:
• ...
• ...

Clinical Notes:
• ...
• ...

Source:
...
"""

        return self.ask(
            prompt
        )

    def health_check(self):

        try:

            response = (
                self.ask(
                    "Reply with OK"
                )
            )

            return {

                "status":
                    "healthy",

                "response":
                    response
            }

        except Exception as e:

            return {

                "status":
                    "error",

                "message":
                    str(e)
            }