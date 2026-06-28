"""
===========================================================
MedShield-X

Chunk Utilities
===========================================================
"""

import hashlib


class ChunkUtils:

    @staticmethod
    def generate_chunk_id(text: str) -> str:
        return hashlib.md5(
            text.encode("utf-8")
        ).hexdigest()

    @staticmethod
    def calculate_chunk_length(text: str):

        return {

            "characters": len(text),

            "words": len(text.split())

        }