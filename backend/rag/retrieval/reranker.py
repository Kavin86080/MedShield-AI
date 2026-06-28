"""
===========================================================
MedShield-X

Simple Reranker
===========================================================
"""


class Reranker:

    def rerank(self, retrieved_chunks):

        retrieved_chunks.sort(

            key=lambda x: x["score"],

            reverse=True

        )

        return retrieved_chunks