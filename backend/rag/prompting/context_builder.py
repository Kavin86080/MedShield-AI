"""
===========================================================
MedShield-X

Context Builder
===========================================================
"""


class ContextBuilder:

    def build(

        self,

        retrieved_chunks

    ):

        context = ""

        for chunk in retrieved_chunks:

            context += chunk["text"]

            context += "\n\n"

        return context.strip()