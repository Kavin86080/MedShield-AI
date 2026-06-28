"""
===========================================================
MedShield-X

Enterprise Dynamic Patient RAG Pipeline

Purpose
-------
Main orchestration pipeline.

Responsibilities
----------------
• Manage consultation session
• Manage uploads
• Manage queries
• Manage shared collection
===========================================================
"""

from backend.rag.collection.collection_manager import CollectionManager

from backend.rag.memory.conversation_memory import ConversationMemory

from backend.rag.pipeline.upload_pipeline import UploadPipeline

from backend.rag.pipeline.query_pipeline import QueryPipeline


class DynamicRAGPipeline:

    def __init__(self):

        # ------------------------------------------
        # Shared objects
        # ------------------------------------------

        self.collection = CollectionManager()

        self.memory = ConversationMemory()

        # ------------------------------------------
        # Pipelines
        # ------------------------------------------

        self.upload = UploadPipeline(

            collection_manager=self.collection

        )

        self.query = QueryPipeline(

            collection_manager=self.collection

        )

    # ------------------------------------------------

    def upload_document(

        self,

        file_path

    ):

        result = self.upload.process_document(

            file_path

        )

        # Rebuild retriever indexes to include the newly uploaded document chunks
        self.query.retriever.build_indexes(

            self.collection.documents.get_all_chunks()

        )

        return {

            "status": "success",

            "message": "Document uploaded successfully.",

            "summary":

                self.collection.collection_summary()

        }

    # ------------------------------------------------

    def ask(

        self,

        question

    ):

        return self.query.ask(

            question

        )

    # ------------------------------------------------

    def get_collection_summary(

        self

    ):

        return self.collection.collection_summary()

    # ------------------------------------------------

    def reset_consultation(

        self

    ):

        self.collection.clear()

        self.memory.clear()

        return {

            "status": "success",

            "message":

                "Consultation reset successfully."

        }