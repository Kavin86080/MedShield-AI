"""
===========================================================
MedShield-X

Enterprise Prompt Builder

Purpose
-------
Construct a structured clinical prompt for the LLM.

Author
------
MedShield-X
===========================================================
"""

from backend.rag.prompting.context_builder import ContextBuilder
from backend.rag.prompting.prompt_templates import PromptTemplates


class PromptBuilder:

    def __init__(self):

        self.context_builder = ContextBuilder()

    def build(

        self,

        question,

        context,

        evidence,

        confidence,

        citations,

        conversation

    ):

        # ------------------------------------------------
        # Build Retrieved Context
        # ------------------------------------------------

        retrieved_context = self.context_builder.build(

            evidence

        )

        # ------------------------------------------------
        # Conversation History
        # ------------------------------------------------

        conversation_text = ""

        for item in conversation:

            conversation_text += (

                f"{item['role'].upper()}: "

                f"{item['content']}\n"

            )

        # ------------------------------------------------
        # Citations
        # ------------------------------------------------

        citation_text = ""

        for citation in citations:

            citation_text += (

                f"- {citation['reference']}\n"

            )

        # ------------------------------------------------
        # Prompt
        # ------------------------------------------------

        user_prompt = f"""
====================================================

CURRENT CONSULTATION

====================================================

Conversation History

{conversation_text}

----------------------------------------------------

Clinical Evidence

----------------------------------------------------

{retrieved_context}

----------------------------------------------------

Evidence Confidence

----------------------------------------------------

{confidence:.2f}

----------------------------------------------------

Evidence Sources

----------------------------------------------------

{citation_text}

----------------------------------------------------

Doctor Question

----------------------------------------------------

{question}

====================================================

Instructions

====================================================

1. Answer only using the provided evidence.

2. Do NOT hallucinate.

3. If evidence is insufficient,
   clearly mention it.

4. Explain your reasoning.

5. Mention possible differential
   diagnoses when appropriate.

6. Mention recommended next
   investigations if required.

7. Mention possible red flags.

====================================================
"""

        return {

            "system": PromptTemplates.SYSTEM_PROMPT,

            "user": user_prompt

        }