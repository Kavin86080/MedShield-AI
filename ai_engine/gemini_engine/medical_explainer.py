from ai_engine.gemini_engine.gemini_service import (
    GeminiService
)


class MedicalExplainer:

    def __init__(self):

        self.gemini = (
            GeminiService()
        )

    def explain(
        self,
        prediction,
        confidence
    ):

        prompt = f"""
You are an expert radiologist.

Chest X-Ray Prediction:
{prediction}

Confidence:
{confidence}%

Provide:

1. Clinical Interpretation
2. Possible Findings
3. Recommendation

Keep response concise.
"""

        return self.gemini.ask(
            prompt
        )