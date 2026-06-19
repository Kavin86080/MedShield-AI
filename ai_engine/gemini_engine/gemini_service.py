from ai_engine.gemini_engine.gemini_client import (
    GeminiClient
)


class GeminiService:

    def __init__(self):

        self.client = GeminiClient()

    def ask(
        self,
        prompt: str
    ) -> str:

        return self.client.generate(
            prompt
        )

    def health_check(self):

        try:

            response = self.ask(
                "Reply with OK"
            )

            return {
                "status": "healthy",
                "response": response
            }

        except Exception as e:

            return {
                "status": "error",
                "message": str(e)
            }