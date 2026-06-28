"""
===========================================================
MedShield-X

Retriever
===========================================================
"""

from backend.rag.embeddings.embedding_model import EmbeddingModel

from backend.rag.retrieval.search_utils import SearchUtils

from backend.rag.retrieval.reranker import Reranker


class Retriever:

    def __init__(

        self,

        faiss_service

    ):

        self.faiss = faiss_service

        self.embedding_model = EmbeddingModel()

        self.reranker = Reranker()

    def retrieve(

        self,

        question,

        top_k=5

    ):

        query_vector = self.embedding_model.encode(

            [question]

        )

        scores, indices = self.faiss.index.search(

            query_vector,

            top_k

        )

        retrieved = SearchUtils.top_k(

            scores,

            indices,

            self.faiss.chunk_store

        )

        retrieved = self.reranker.rerank(

            retrieved

        )

        return retrieved