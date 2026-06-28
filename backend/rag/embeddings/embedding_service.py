"""
===========================================================
MedShield-X

Embedding Service
===========================================================
"""

from backend.rag.embeddings.embedding_model import EmbeddingModel

from backend.rag.embeddings.embedding_utils import EmbeddingUtils


class EmbeddingService:

    def __init__(self):

        self.model = EmbeddingModel()

    def generate_embeddings(

        self,

        document

    ):

        chunks = document["chunks"]

        texts = [

            chunk["text"]

            for chunk in chunks

        ]

        vectors = self.model.encode(

            texts

        )

        embeddings = []

        for chunk, vector in zip(

            chunks,

            vectors

        ):

            embeddings.append(

                {

                    "chunk_id": chunk["chunk_id"],

                    "chunk_index": chunk["chunk_index"],

                    "document_id": document["metadata"]["document_id"],

                    "embedding": EmbeddingUtils.normalize(

                        vector

                    ),

                    "dimension": EmbeddingUtils.embedding_dimension(

                        vector

                    ),

                    "text": chunk["text"]

                }

            )

        document["embeddings"] = embeddings

        return document