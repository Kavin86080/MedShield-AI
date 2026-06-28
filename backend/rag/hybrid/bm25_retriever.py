"""
===========================================================
MedShield-X

BM25 Retriever

Purpose
-------
Keyword-based retrieval for Hybrid RAG.

Author
------
MedShield-X
===========================================================
"""

from rank_bm25 import BM25Okapi
import nltk


class BM25Retriever:

    def __init__(self):

        self.bm25 = None

        self.documents = []

        self.tokenized_documents = []

    def build_index(
        self,
        chunks: list
    ):

        """
        Build BM25 index from chunk list.
        """

        self.documents = chunks

        if not chunks:
            self.tokenized_documents = []
            self.bm25 = None
            return

        self.tokenized_documents = [

            nltk.word_tokenize(
                chunk["text"].lower()
            )

            for chunk in chunks

        ]

        self.bm25 = BM25Okapi(

            self.tokenized_documents

        )

    def retrieve(

        self,

        query: str,

        top_k: int = 5

    ):

        if self.bm25 is None or not self.documents:
            return []

        tokenized_query = nltk.word_tokenize(

            query.lower()

        )

        scores = self.bm25.get_scores(

            tokenized_query

        )

        ranked = sorted(

            zip(

                self.documents,

                scores

            ),

            key=lambda x: x[1],

            reverse=True

        )

        results = []

        for chunk, score in ranked[:top_k]:

            results.append(

                {

                    "retrieval_type": "bm25",

                    "score": float(score),

                    "chunk_id": chunk["chunk_id"],

                    "chunk_index": chunk["chunk_index"],

                    "document_id": chunk["document_id"],

                    "text": chunk["text"]

                }

            )

        return results
         