import faiss
import numpy as np


class FAISSStore:

    def __init__(
        self,
        embedding_dimension=384
    ):

        self.dimension = embedding_dimension

        self.index = faiss.IndexFlatL2(
            embedding_dimension
        )

        self.documents = []

    def add_documents(
        self,
        documents,
        embeddings
    ):

        embeddings = np.array(
            embeddings,
            dtype=np.float32
        )

        self.index.add(
            embeddings
        )

        self.documents.extend(
            documents
        )

    def search(
        self,
        query_embedding,
        top_k=3
    ):

        query_embedding = np.array(
            [query_embedding],
            dtype=np.float32
        )

        distances, indices = (
            self.index.search(
                query_embedding,
                top_k
            )
        )

        results = []

        for idx in indices[0]:

            if idx < len(self.documents):

                results.append(
                    self.documents[idx]
                )

        return results

    def total_documents(self):

        return len(
            self.documents
        )