"""
===========================================================
MedShield-X

LLM Factory
===========================================================
"""

from backend.rag.llm.groq_service import GroqService


class LLMFactory:

    @staticmethod
    def create():

        return GroqService()