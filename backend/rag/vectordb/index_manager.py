"""
===========================================================
MedShield-X

Index Manager
===========================================================
"""

import faiss


class IndexManager:

    def __init__(

        self,

        dimension

    ):

        self.index = faiss.IndexFlatIP(

            dimension

        )

    def add(

        self,

        vectors

    ):

        self.index.add(vectors)

    def search(

        self,

        query,

        k=5

    ):

        scores, indices = self.index.search(

            query,

            k

        )

        return scores, indices

    def save(

        self,

        path

    ):

        faiss.write_index(

            self.index,

            path

        )

    def load(

        self,

        path

    ):

        self.index = faiss.read_index(

            path

        )