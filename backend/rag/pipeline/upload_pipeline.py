"""
===========================================================
MedShield-X

Enterprise Upload Pipeline

Purpose
-------
Complete document ingestion pipeline.

Flow
----
Upload
    ↓
Document Loader
    ↓
Cleaner
    ↓
Metadata Generator
    ↓
Adaptive Chunker
    ↓
Embedding Generator
    ↓
FAISS Index
    ↓
BM25 Index
===========================================================
"""

from backend.rag.ingestion.document_loader import DocumentLoader

from backend.rag.preprocessing.cleaner import TextCleaner

from backend.rag.preprocessing.metadata import MetadataGenerator

from backend.rag.chunking.adaptive_chunker import AdaptiveChunker

from backend.rag.embeddings.embedding_service import EmbeddingService

from backend.rag.collection.collection_manager import CollectionManager

class UploadPipeline:

    def __init__(

        self,

        collection_manager=None

    ):

        self.loader = DocumentLoader()

        self.cleaner = TextCleaner()

        self.metadata = MetadataGenerator()

        self.chunker = AdaptiveChunker()

        self.embedding = EmbeddingService()

        self.collection = (

            collection_manager

            if collection_manager

            else CollectionManager()

        )

    def process_document(

        self,

        file_path: str

    ):

        # ------------------------------------------------
        # Load Document
        # ------------------------------------------------

        document = self.loader.load_document(

            file_path

        )

        # ------------------------------------------------
        # Clean Text
        # ------------------------------------------------

        document = self.cleaner.clean(

            document

        )

        # ------------------------------------------------
        # Metadata
        # ------------------------------------------------

        document = self.metadata.process(

            document

        )

        # ------------------------------------------------
        # Chunking
        # ------------------------------------------------

        document = self.chunker.chunk(

            document

        )

        # ------------------------------------------------
        # Embeddings
        # ------------------------------------------------

        document = self.embedding.generate_embeddings(

            document

        )

        # ------------------------------------------------
        # Add document to collection
        # ------------------------------------------------

        self.collection.add_document(

            document

        )

        return {

    "status": "success",

    "message": "Document processed successfully.",

    "document": document,

    "collection": self.collection,

    "summary":

        self.collection.collection_summary()

    }