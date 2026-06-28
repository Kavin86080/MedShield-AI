"""
===========================================================
MedShield-X

Conversation Memory

Stores doctor conversation history.
===========================================================
"""


class ConversationMemory:

    def __init__(self):

        self.history = []

    def add_message(

        self,

        role,

        content

    ):

        self.history.append(

            {

                "role": role,

                "content": content

            }

        )

    def get_history(self):

        return self.history

    def clear(self):

        self.history = []