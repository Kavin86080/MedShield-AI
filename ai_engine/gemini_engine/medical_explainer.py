from ai_engine.groq_engine.groq_service import (
    GroqService
)


class MedicalExplainer:

    def __init__(self):

        self.llm = (
            GroqService()
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

Keep response concise and professional.

Output Format:

Clinical Interpretation:
...

Possible Findings:
• ...
• ...

Recommendation:
• ...
• ...
"""

        return self.llm.ask(
            prompt
        )