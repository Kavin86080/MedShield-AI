"""
===========================================================
MedShield-X
Dynamic Patient RAG

File:
    pdf_loader.py

Purpose:
    Production-ready PDF Loader

Features:
    ✔ PDF Text Extraction
    ✔ Page-wise Extraction
    ✔ Metadata Extraction
    ✔ Document UUID
    ✔ Session UUID
    ✔ Upload Timestamp
    ✔ File Size
    ✔ Processing Time
    ✔ OCR Detection
    ✔ Document Statistics
    ✔ Error Handling

Author:
    MedShield-X
===========================================================
"""

from pathlib import Path
from uuid import uuid4
from datetime import datetime
import time

import fitz


class PDFLoader:
    """
    Production-ready PDF Loader
    """

    def load(
        self,
        file_path: str
    ) -> dict:

        file = Path(file_path)

        if not file.exists():
            raise FileNotFoundError(
                f"PDF file not found: {file_path}"
            )

        start_time = time.time()

        try:

            document = fitz.open(file_path)

            pages = []

            full_text = []

            for page_number in range(len(document)):

                page = document.load_page(page_number)

                text = page.get_text("text").strip()

                # Ignore completely empty pages
                if not text:
                    continue

                pages.append(
                    {
                        "page": page_number + 1,
                        "text": text
                    }
                )

                full_text.append(text)

            processing_time = round(
                time.time() - start_time,
                3
            )

            metadata = {

                # Unique IDs
                "document_id": str(uuid4()),
                

                # File Information
                "file_name": file.name,
                "file_path": str(file.resolve()),
                "file_type": ".pdf",
                "file_size": file.stat().st_size,

                # PDF Metadata
                "total_pages": len(document),
                "title": document.metadata.get("title"),
                "author": document.metadata.get("author"),
                "subject": document.metadata.get("subject"),
                "creator": document.metadata.get("creator"),
                "producer": document.metadata.get("producer"),

                # Processing Information
                "uploaded_at": datetime.utcnow().isoformat(),
                "processing_time": processing_time,

                # Source Information
                "source_type": "doctor_upload",

                # OCR Detection
                "ocr_required": len(full_text) == 0

            }

            statistics = {

                "page_count": len(document),

                "non_empty_pages": len(pages),

                "character_count": len(
                    "\n".join(full_text)
                ),

                "word_count": len(
                    "\n".join(full_text).split()
                )

            }

            document.close()

            return {

                "status": "success",

                "document_text": "\n".join(full_text),

                "pages": pages,

                "metadata": metadata,

                "statistics": statistics

            }

        except Exception as e:

            raise RuntimeError(
                f"Unable to process PDF: {e}"
            )