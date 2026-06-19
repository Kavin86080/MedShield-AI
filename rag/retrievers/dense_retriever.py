# Placeholder for dense_retriever.py
from rag.embeddings.sentence_transformer_embedder import (
    SentenceTransformerEmbedder
)

from vector_store.faiss_store import (
    FAISSStore
)


class DenseRetriever:

    def __init__(
        self,
        embedder=None,
        vector_store=None
    ):

        self.embedder = (
            embedder
            if embedder
            else SentenceTransformerEmbedder()
        )

        self.vector_store = (
            vector_store
            if vector_store
            else FAISSStore()
        )

    def index_documents(
        self,
        documents
    ):
        """
        Generate embeddings and store them in FAISS
        """

        embeddings = (
            self.embedder.embed_documents(
                documents
            )
        )

        self.vector_store.add_documents(
            documents,
            embeddings
        )

    def retrieve(
        self,
        query,
        top_k=3
    ):
        """
        Retrieve most relevant chunks
        """

        query_embedding = (
            self.embedder.embed_text(
                query
            )
        )

        results = (
            self.vector_store.search(
                query_embedding,
                top_k=top_k
            )
        )

        return results

    def total_documents(
        self
    ):
        return (
            self.vector_store.total_documents()
        )