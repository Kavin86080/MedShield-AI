"""
===========================================================
MedShield-X

BM25 Collection

Purpose
-------
Maintain a growing BM25 index for all uploaded
documents within a consultation.

Supports:
    • Incremental document addition
    • Keyword retrieval
===========================================================
"""

from rank_bm25 import BM25Okapi
import nltk


class BM25Collection:

    def __init__(self):

        self.documents = []

        self.tokenized_documents = []

        self.bm25 = None

    # -----------------------------------------------------

    def add_document(

        self,

        document

    ):

        chunks = document["chunks"]

        for chunk in chunks:

            self.documents.append(

                {

                    "chunk_id": chunk["chunk_id"],

                    "document_id": document["metadata"]["document_id"],

                    "chunk_index": chunk["chunk_index"],

                    "text": chunk["text"]

                }

            )

        self._rebuild()

    # -----------------------------------------------------

    def _rebuild(

        self

    ):

        if not self.documents:
            self.tokenized_documents = []
            self.bm25 = None
            return

        self.tokenized_documents = [

            nltk.word_tokenize(

                item["text"].lower()

            )

            for item in self.documents

        ]

        self.bm25 = BM25Okapi(

            self.tokenized_documents

        )

    # -----------------------------------------------------

    def search(

        self,

        query,

        top_k=5

    ):

        if self.bm25 is None:

            return []

        tokens = nltk.word_tokenize(

            query.lower()

        )

        scores = self.bm25.get_scores(

            tokens

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

        for item, score in ranked[:top_k]:

            results.append(

                {

                    "score": float(score),

                    **item

                }

            )

        return results

    # -----------------------------------------------------

    def total_chunks(

        self

    ):

        return len(

            self.documents

        )

    # -----------------------------------------------------

    def clear(

        self

    ):

        self.documents = []

        self.tokenized_documents = []

        self.bm25 = None