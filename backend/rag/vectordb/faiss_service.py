"""
===========================================================
MedShield-X

FAISS Service
===========================================================
"""

import os

from backend.rag.vectordb.index_manager import IndexManager
from backend.rag.vectordb.vector_utils import VectorUtils


class FAISSService:

    def __init__(self):

        self.index = None

        self.chunk_store = []

    def build_index(

        self,

        document

    ):

        embeddings = document["embeddings"]

        vectors = [

            item["embedding"]

            for item in embeddings

        ]

        vectors = VectorUtils.to_numpy(

            vectors

        )

        vectors = VectorUtils.normalize(

            vectors

        )

        dimension = vectors.shape[1]

        self.index = IndexManager(

            dimension

        )

        self.index.add(

            vectors

        )

        self.chunk_store = embeddings

        return document

    def save(

        self,

        folder="datasets/vector_store"

    ):

        os.makedirs(

            folder,

            exist_ok=True

        )

        self.index.save(

            os.path.join(

                folder,

                "faiss.index"

            )

        )

    def load(

        self,

        folder="datasets/vector_store"

    ):

        self.index = IndexManager(

            768

        )

        self.index.load(

            os.path.join(

                folder,

                "faiss.index"

            )

        )