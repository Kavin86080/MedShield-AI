"""
===========================================================
MedShield-X

Collection Metadata

Purpose
-------
Stores metadata for the entire document collection.

Author
------
MedShield-X
===========================================================
"""

from uuid import uuid4
from datetime import datetime


class CollectionMetadata:

    def __init__(self):

        self.collection_id = str(uuid4())

        self.session_id = str(uuid4())

        self.created_at = datetime.utcnow().isoformat()

        self.updated_at = self.created_at

        self.total_documents = 0

        self.total_chunks = 0

        self.total_embeddings = 0

        self.total_vectors = 0

        self.file_types = set()

        self.document_ids = []

        self.collection_status = "ACTIVE"

    # -------------------------------------------------

    def update(

        self,

        document

    ):

        metadata = document["metadata"]

        self.updated_at = datetime.utcnow().isoformat()

        self.total_documents += 1

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

        self.total_vectors = self.total_embeddings

        self.document_ids.append(

            metadata["document_id"]

        )

        self.file_types.add(

            metadata["file_type"]

        )

    # -------------------------------------------------

    def remove(

        self,

        document

    ):

        metadata = document["metadata"]

        self.updated_at = datetime.utcnow().isoformat()

        self.total_documents -= 1

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

        self.total_vectors = self.total_embeddings

        if metadata["document_id"] in self.document_ids:

            self.document_ids.remove(

                metadata["document_id"]

            )

    # -------------------------------------------------

    def get_metadata(

        self

    ):

        return {

            "collection_id": self.collection_id,

            "session_id": self.session_id,

            "created_at": self.created_at,

            "updated_at": self.updated_at,

            "status": self.collection_status,

            "documents": self.total_documents,

            "chunks": self.total_chunks,

            "embeddings": self.total_embeddings,

            "vectors": self.total_vectors,

            "file_types": list(

                self.file_types

            ),

            "document_ids": self.document_ids

        }

    # -------------------------------------------------

    def close(

        self

    ):

        self.collection_status = "CLOSED"

        self.updated_at = datetime.utcnow().isoformat()

    # -------------------------------------------------

    def reset(

        self

    ):

        self.__init__()