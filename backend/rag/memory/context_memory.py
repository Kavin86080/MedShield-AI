"""
===========================================================
MedShield-X

Context Memory

Builds conversation context.
===========================================================
"""


class ContextMemory:

    def build(

        self,

        history,

        max_turns=5

    ):

        context = ""

        recent = history[-max_turns:]

        for message in recent:

            context += (

                f"{message['role']}: "

                f"{message['content']}\n"

            )

        return context