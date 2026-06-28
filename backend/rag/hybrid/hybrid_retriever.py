"""
===========================================================
MedShield-X

Hybrid Retriever

Purpose
-------
FAISS
+
BM25
+
Fusion
+
Cross Encoder

Final Retrieval Pipeline
===========================================================
"""

from backend.rag.retrieval.retriever import Retriever

from backend.rag.hybrid.bm25_retriever import BM25Retriever

from backend.rag.hybrid.fusion import HybridFusion

from backend.rag.hybrid.cross_encoder import CrossEncoderReranker


class HybridRetriever:

    def __init__(

        self,

        faiss_service

    ):

        self.faiss = Retriever(

            faiss_service

        )

        self.bm25 = BM25Retriever()

        self.fusion = HybridFusion()

        self.cross_encoder = CrossEncoderReranker()

        self.initialized = False

    def build_indexes(

        self,

        chunk_store

    ):

        """
        Build BM25 index.

        FAISS index already exists.
        """

        self.bm25.build_index(

            chunk_store

        )

        self.initialized = True

    def retrieve(

        self,

        question,

        top_k=5

    ):

        if not self.initialized:

            raise Exception(

                "Hybrid Retriever has not been initialized."

            )

        # -----------------------------------
        # FAISS Retrieval
        # -----------------------------------

        faiss_results = self.faiss.retrieve(

            question,

            top_k=10

        )

        # -----------------------------------
        # BM25 Retrieval
        # -----------------------------------

        bm25_results = self.bm25.retrieve(

            question,

            top_k=10

        )

        # -----------------------------------
        # Hybrid Fusion
        # -----------------------------------

        fused_results = self.fusion.fuse(

            faiss_results,

            bm25_results

        )

        # -----------------------------------
        # Cross Encoder
        # -----------------------------------

        reranked = self.cross_encoder.rerank(

            question,

            fused_results,

            top_k=top_k

        )

        return {

            "question": question,

            "faiss_results": faiss_results,

            "bm25_results": bm25_results,

            "fused_results": fused_results,

            "final_results": reranked

        }