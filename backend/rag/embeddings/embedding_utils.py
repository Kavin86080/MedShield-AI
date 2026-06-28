"""
===========================================================
MedShield-X

Embedding Utilities
===========================================================
"""

import numpy as np


class EmbeddingUtils:

    @staticmethod
    def normalize(vector):

        vector = np.array(vector)

        norm = np.linalg.norm(vector)

        if norm == 0:

            return vector.tolist()

        return (vector / norm).tolist()

    @staticmethod
    def embedding_dimension(vector):

        return len(vector)