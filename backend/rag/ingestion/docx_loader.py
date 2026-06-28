"""
===========================================================
MedShield-X
Dynamic Patient RAG

File:
    docx_loader.py

Purpose:
    Production-ready DOCX Loader

Features:
    ✔ DOCX Text Extraction
    ✔ Paragraph Extraction
    ✔ Metadata
    ✔ UUID
    ✔ Statistics
    ✔ Error Handling

Author:
    MedShield-X
===========================================================
"""

from pathlib import Path
from uuid import uuid4
from datetime import datetime
import time

from docx import Document


class DOCXLoader:
    """
    Production-ready DOCX Loader.
    """

    def load(
        self,
        file_path: str
    ) -> dict:

        file = Path(file_path)

        if not file.exists():
            raise FileNotFoundError(
                f"DOCX file not found: {file_path}"
            )

        start_time = time.time()

        try:

            document = Document(file_path)

            paragraphs = []

            full_text = []

            for index, paragraph in enumerate(document.paragraphs):

                text = paragraph.text.strip()

                if not text:
                    continue

                paragraphs.append(
                    {
                        "paragraph": index + 1,
                        "text": text
                    }
                )

                full_text.append(text)

            document_text = "\n".join(full_text)

            processing_time = round(
                time.time() - start_time,
                3
            )

            metadata = {

                "document_id": str(uuid4()),

                "file_name": file.name,

                "file_path": str(file.resolve()),

                "file_type": ".docx",

                "file_size": file.stat().st_size,

                "paragraphs": len(paragraphs),

                "uploaded_at": datetime.utcnow().isoformat(),

                "processing_time": processing_time,

                "source_type": "doctor_upload"

            }

            statistics = {

                "paragraph_count": len(paragraphs),

                "character_count": len(document_text),

                "word_count": len(document_text.split())

            }

            return {

                "status": "success",

                "text": document_text,

                "paragraphs": paragraphs,

                "metadata": metadata,

                "statistics": statistics

            }

        except Exception as e:

            raise RuntimeError(
                f"Unable to process DOCX: {e}"
            )