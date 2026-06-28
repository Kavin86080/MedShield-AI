import os
import time

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
                "GEMINI_API_KEY not found."
            )

        genai.configure(
            api_key=api_key
        )

        model_name = os.getenv(
            "GEMINI_MODEL",
            "gemini-1.5-flash"
        )

        self.model = (
            genai.GenerativeModel(
                model_name
            )
        )

    def generate(
        self,
        prompt: str,
        retries: int = 3
    ) -> str:

        for attempt in range(
            retries
        ):

            try:

                response = (
                    self.model.generate_content(
                        prompt
                    )
                )

                if hasattr(
                    response,
                    "text"
                ):

                    return response.text

                return str(
                    response
                )

            except Exception as e:

                print(
                    f"Gemini Attempt {attempt+1} Failed: {e}"
                )

                time.sleep(
                    2
                )

        return (
            "Unable to generate response from Gemini."
        )