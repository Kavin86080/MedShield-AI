"""
===========================================================
MedShield-X

Dynamic Patient RAG

Text Cleaner

Purpose
-------
Clean extracted document text before chunking.
===========================================================
"""

import re
import unicodedata


class TextCleaner:

    def clean(
        self,
        document: dict
    ) -> dict:

        text = document["text"]

        # Normalize Unicode
        text = unicodedata.normalize("NFKC", text)

        # Remove multiple spaces
        text = re.sub(r"\s+", " ", text)

        # Remove multiple blank lines
        text = re.sub(r"\n+", "\n", text)

        # Remove tabs
        text = text.replace("\t", " ")

        # Remove extra spaces
        text = text.strip()

        document["clean_text"] = text

        return document