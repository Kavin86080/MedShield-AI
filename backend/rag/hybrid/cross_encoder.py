"""
===========================================================
MedShield-X

Cross Encoder Reranker

Purpose
-------
Re-rank Hybrid Retrieval results using a
CrossEncoder model.

Author
------
MedShield-X
===========================================================
"""

from sentence_transformers import CrossEncoder


class CrossEncoderReranker:

    def __init__(self):

        self.model = CrossEncoder(

            "cross-encoder/ms-marco-MiniLM-L-6-v2"

        )

    def rerank(

        self,

        question: str,

        retrieved_chunks: list,

        top_k: int = 5

    ):

        if len(retrieved_chunks) == 0:

            return []

        sentence_pairs = [

            (

                question,

                chunk["text"]

            )

            for chunk in retrieved_chunks

        ]

        scores = self.model.predict(

            sentence_pairs

        )

        reranked = []

        for chunk, score in zip(

            retrieved_chunks,

            scores

        ):

            item = chunk.copy()

            item["cross_encoder_score"] = float(score)

            reranked.append(item)

        reranked.sort(

            key=lambda x: x["cross_encoder_score"],

            reverse=True

        )

        return reranked[:top_k]