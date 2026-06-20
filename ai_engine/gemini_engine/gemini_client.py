import os

import google.generativeai as genai

from dotenv import load_dotenv

load_dotenv()

class GeminiClient:

    def __init__(self):

        api_key = os.getenv(
            "GEMINI_API_KEY"
        )

        if not api_key:

            raise ValueError(
                "GEMINI_API_KEY not found in environment variables."
            )

        genai.configure(
            api_key=api_key
        )

        model_name = os.getenv(
            "GEMINI_MODEL",
            "models/gemini-2.5-flash"
        )

        self.model = genai.GenerativeModel(
            model_name=model_name
        )

    def generate(
        self,
        prompt: str
    ) -> str:

        response = self.model.generate_content(
            prompt
        )

        return response.text