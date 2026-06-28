"""
===========================================================
MedShield-X

Adaptive Chunker
===========================================================
"""

from backend.rag.chunking.semantic_chunker import SemanticChunker


class AdaptiveChunker:

    def chunk(

        self,

        document: dict

    ):

        words = len(

            document["clean_text"].split()

        )

        if words < 500:

            chunk_size = 400

            overlap = 50

        elif words < 3000:

            chunk_size = 800

            overlap = 100

        else:

            chunk_size = 1200

            overlap = 200

        chunker = SemanticChunker(

            chunk_size=chunk_size,

            chunk_overlap=overlap

        )

        return chunker.chunk(document)