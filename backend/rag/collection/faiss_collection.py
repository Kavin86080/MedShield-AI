"""
===========================================================
MedShield-X

FAISS Collection

Purpose
-------
Maintain a single FAISS index for all uploaded
documents within a consultation.

Supports:
    • Incremental indexing
    • Similarity search
    • Save / Load
===========================================================
"""

import os
import pickle
import numpy as np
import faiss


class FAISSCollection:

    def __init__(

        self,

        dimension=768

    ):

        self.dimension = dimension

        self.index = faiss.IndexFlatIP(

            dimension

        )

        self.chunk_store = []

        self.document_store = []

    # --------------------------------------------------

    def add_document(

        self,

        document

    ):

        embeddings = document["embeddings"]

        vectors = np.array(

            [

                item["embedding"]

                for item in embeddings

            ],

            dtype=np.float32

        )

        faiss.normalize_L2(vectors)

        self.index.add(vectors)

        for item in embeddings:

            self.chunk_store.append(

                {

                    "chunk_id": item["chunk_id"],

                    "document_id": item["document_id"],

                    "chunk_index": item["chunk_index"],

                    "text": item["text"]

                }

            )

        self.document_store.append(

            document["metadata"]["document_id"]

        )

    # --------------------------------------------------

    def search(

        self,

        query_vector,

        top_k=5

    ):

        query = np.array(

            query_vector,

            dtype=np.float32

        )

        faiss.normalize_L2(query)

        scores, indices = self.index.search(

            query,

            top_k

        )

        results = []

        for score, idx in zip(

            scores[0],

            indices[0]

        ):

            if idx == -1:

                continue

            chunk = self.chunk_store[idx]

            results.append(

                {

                    "score": float(score),

                    **chunk

                }

            )

        return results

    # --------------------------------------------------

    def save(

        self,

        folder="datasets/vector_store"

    ):

        os.makedirs(

            folder,

            exist_ok=True

        )

        faiss.write_index(

            self.index,

            os.path.join(

                folder,

                "collection.index"

            )

        )

        with open(

            os.path.join(

                folder,

                "collection.pkl"

            ),

            "wb"

        ) as f:

            pickle.dump(

                self.chunk_store,

                f

            )

    # --------------------------------------------------

    def load(

        self,

        folder="datasets/vector_store"

    ):

        self.index = faiss.read_index(

            os.path.join(

                folder,

                "collection.index"

            )

        )

        with open(

            os.path.join(

                folder,

                "collection.pkl"

            ),

            "rb"

        ) as f:

            self.chunk_store = pickle.load(

                f

            )

    # --------------------------------------------------

    def total_vectors(

        self

    ):

        return self.index.ntotal

    # --------------------------------------------------

    def clear(

        self

    ):

        self.index = faiss.IndexFlatIP(

            self.dimension

        )

        self.chunk_store = []

        self.document_store = []