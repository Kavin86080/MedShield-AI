"""
===========================================================
MedShield-X

Document Collection

Purpose
-------
Maintain all uploaded documents, chunks,
embeddings and metadata for a consultation.

Author
------
MedShield-X
===========================================================
"""

from uuid import uuid4
from datetime import datetime


class DocumentCollection:

    def __init__(self):

        self.collection_id = str(uuid4())

        self.created_at = datetime.utcnow().isoformat()

        self.documents = {}

        self.total_documents = 0

        self.total_chunks = 0

        self.total_embeddings = 0

    # -------------------------------------------------

    def add_document(

        self,

        document: dict

    ):

        document_id = document["metadata"]["document_id"]

        self.documents[document_id] = document

        self.total_documents = len(self.documents)

        self.total_chunks += len(

            document.get(

                "chunks",

                []

            )

        )

        self.total_embeddings += len(

            document.get(

                "embeddings",

                []

            )

        )

    # -------------------------------------------------

    def remove_document(

        self,

        document_id

    ):

        if document_id not in self.documents:

            return False

        document = self.documents.pop(

            document_id

        )

        self.total_documents = len(self.documents)

        self.total_chunks -= len(

            document.get(

                "chunks",

                []

            )

        )

        self.total_embeddings -= len(

            document.get(

                "embeddings",

                []

            )

        )

        return True

    # -------------------------------------------------

    def get_document(

        self,

        document_id

    ):

        return self.documents.get(

            document_id

        )

    # -------------------------------------------------

    def get_all_documents(

        self

    ):

        return list(

            self.documents.values()

        )

    # -------------------------------------------------

    def get_all_chunks(

        self

    ):

        chunks = []

        for document in self.documents.values():

            chunks.extend(

                document.get(

                    "chunks",

                    []

                )

            )

        return chunks

    # -------------------------------------------------

    def get_all_embeddings(

        self

    ):

        embeddings = []

        for document in self.documents.values():

            embeddings.extend(

                document.get(

                    "embeddings",

                    []

                )

            )

        return embeddings

    # -------------------------------------------------

    def summary(

        self

    ):

        return {

            "collection_id": self.collection_id,

            "created_at": self.created_at,

            "documents": self.total_documents,

            "chunks": self.total_chunks,

            "embeddings": self.total_embeddings

        }

    # -------------------------------------------------

    def clear(self):

        self.documents.clear()

        self.total_documents = 0

        self.total_chunks = 0

        self.total_embeddings = 0