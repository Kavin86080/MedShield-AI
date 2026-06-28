"""
===========================================================
MedShield-X

Enterprise Groq Service

Author:
    MedShield-X
===========================================================
"""

import os
import time

from groq import Groq
from dotenv import load_dotenv

from backend.rag.llm.response_parser import ResponseParser

load_dotenv(override=True)


class GroqService:

    def __init__(self):

        self.client = Groq(
            api_key=os.getenv("GROQ_API_KEY")
        )

        self.model = os.getenv(
            "GROQ_MODEL",
            "llama-3.3-70b-versatile"
        )

        self.temperature = float(
            os.getenv(
                "GROQ_TEMPERATURE",
                "0.2"
            )
        )

        self.max_tokens = int(
            os.getenv(
                "GROQ_MAX_TOKENS",
                "1024"
            )
        )

        self.parser = ResponseParser()

    def generate(

        self,

        prompt: dict,

        confidence=None,

        evidence=None,

        citations=None

    ):

        start = time.time()

        response = self.client.chat.completions.create(

            model=self.model,

            messages=[

                {
                    "role": "system",
                    "content": prompt["system"]
                },

                {
                    "role": "user",
                    "content": prompt["user"]
                }

            ],

            temperature=self.temperature,

            max_tokens=self.max_tokens

        )

        response_time = round(

            time.time() - start,

            3

        )

        answer = response.choices[0].message.content

        usage = response.usage

        return {

            "status": "success",

            "answer": self.parser.parse(answer),

            "confidence": confidence,

            "citations": citations if citations else [],

            "evidence": evidence if evidence else [],

            "model": self.model,

            "response_time": response_time,

            "prompt_tokens": getattr(
                usage,
                "prompt_tokens",
                0
            ),

            "completion_tokens": getattr(
                usage,
                "completion_tokens",
                0
            ),

            "total_tokens": getattr(
                usage,
                "total_tokens",
                0
            )

        }