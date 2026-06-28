"""
===========================================================
MedShield-X

Session Memory

Stores current consultation session.
===========================================================
"""

from uuid import uuid4


class SessionMemory:

    def __init__(self):

        self.sessions = {}

    def create_session(self):

        session_id = str(uuid4())

        self.sessions[session_id] = {

            "documents": [],

            "questions": [],

            "answers": []

        }

        return session_id

    def add_document(

        self,

        session_id,

        document_id

    ):

        self.sessions[session_id]["documents"].append(

            document_id

        )

    def add_question(

        self,

        session_id,

        question

    ):

        self.sessions[session_id]["questions"].append(

            question

        )

    def add_answer(

        self,

        session_id,

        answer

    ):

        self.sessions[session_id]["answers"].append(

            answer

        )

    def get_session(

        self,

        session_id

    ):

        return self.sessions.get(

            session_id

        )