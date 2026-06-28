"""
===========================================================
MedShield-X

Search Utilities
===========================================================
"""

import numpy as np


class SearchUtils:

    @staticmethod
    def top_k(scores, indices, chunk_store):

        results = []

        for score, index in zip(scores[0], indices[0]):

            if index == -1:
                continue

            chunk = chunk_store[index]

            results.append({

                "score": float(score),

                "chunk_id": chunk["chunk_id"],

                "document_id": chunk["document_id"],

                "chunk_index": chunk["chunk_index"],

                "text": chunk["text"]

            })

        return results