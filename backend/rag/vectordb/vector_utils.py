"""
===========================================================
MedShield-X

Vector Utilities
===========================================================
"""

import numpy as np


class VectorUtils:

    @staticmethod
    def to_numpy(embeddings):

        return np.array(
            embeddings,
            dtype=np.float32
        )

    @staticmethod
    def normalize(vectors):

        vectors = np.array(
            vectors,
            dtype=np.float32
        )

        norms = np.linalg.norm(
            vectors,
            axis=1,
            keepdims=True
        )

        return vectors / norms