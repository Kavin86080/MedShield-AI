"""
===========================================================
MedShield-X

Collection Manager

Purpose
-------
Central manager for a consultation collection.

Responsibilities
----------------
• Manage uploaded documents
• Manage FAISS collection
• Manage BM25 collection
• Manage metadata
===========================================================
"""

from backend.rag.collection.document_collection import DocumentCollection
from backend.rag.collection.faiss_collection import FAISSCollection
from backend.rag.collection.bm25_collection import BM25Collection
from backend.rag.collection.collection_metadata import CollectionMetadata


class CollectionManager:

    def __init__(self):

        self.documents = DocumentCollection()

        self.faiss = FAISSCollection()

        self.bm25 = BM25Collection()

        self.metadata = CollectionMetadata()

    # ------------------------------------------------------

    def add_document(
        self,
        document
    ):

        # Store full document
        self.documents.add_document(
            document
        )

        # Add vectors
        self.faiss.add_document(
            document
        )

        # Add BM25 chunks
        self.bm25.add_document(
            document
        )

        # Update metadata
        self.metadata.update(
            document
        )

    # ------------------------------------------------------

    def remove_document(
        self,
        document_id
    ):

        document = self.documents.get_document(
            document_id
        )

        if document is None:

            return False

        self.documents.remove_document(
            document_id
        )

        # NOTE:
        # FAISS cannot efficiently delete vectors from
        # IndexFlatIP.
        #
        # For now we rebuild the collections.
        #
        # Later we will replace IndexFlatIP with
        # IndexIDMap2 or HNSW.

        self.rebuild()

        return True

    # ------------------------------------------------------

    def rebuild(self):

        all_documents = self.documents.get_all_documents()

        self.faiss = FAISSCollection()

        self.bm25 = BM25Collection()

        self.metadata = CollectionMetadata()

        for document in all_documents:

            self.faiss.add_document(
                document
            )

            self.bm25.add_document(
                document
            )

            self.metadata.update(
                document
            )

    # ------------------------------------------------------

    def semantic_search(
        self,
        query_vector,
        top_k=5
    ):

        return self.faiss.search(
            query_vector,
            top_k
        )

    # ------------------------------------------------------

    def keyword_search(
        self,
        query,
        top_k=5
    ):

        return self.bm25.search(
            query,
            top_k
        )

    # ------------------------------------------------------

    def collection_summary(self):

        return {

            "metadata": self.metadata.get_metadata(),

            "documents": self.documents.summary(),

            "total_vectors": self.faiss.total_vectors(),

            "total_keyword_chunks": self.bm25.total_chunks()

        }

    # ------------------------------------------------------

    def clear(self):

        self.documents.clear()

        self.faiss.clear()

        self.bm25.clear()

        self.metadata.reset()