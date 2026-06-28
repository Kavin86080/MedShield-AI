"""
===========================================================
MedShield-X

Embedding Model
===========================================================
"""

from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self):

        self.model = SentenceTransformer(

            "BAAI/bge-base-en-v1.5"

        )

    def encode(

        self,

        texts

    ):

        return self.model.encode(

            texts,

            convert_to_numpy=True,

            normalize_embeddings=True

        )