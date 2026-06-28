"""
===========================================================
MedShield-X

Dynamic Patient RAG

Metadata Generator

Purpose
-------
Generate metadata required for RAG.
===========================================================
"""

import re


class MetadataGenerator:

    def process(
        self,
        document: dict
    ) -> dict:

        text = document["clean_text"]

        metadata = document["metadata"]

        metadata["word_count"] = len(text.split())

        metadata["character_count"] = len(text)

        metadata["sentence_count"] = len(
            re.findall(r"[.!?]", text)
        )

        metadata["paragraph_count"] = len(
            text.split("\n")
        )

        metadata["contains_tables"] = "|" in text

        metadata["contains_numbers"] = any(
            c.isdigit()
            for c in text
        )

        document["metadata"] = metadata

        return document 