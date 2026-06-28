"""
===========================================================
MedShield-X

OCR Loader

Extracts text from images
===========================================================
"""

from pathlib import Path
from uuid import uuid4
from datetime import datetime
import time

import cv2
import pytesseract


class OCRLoader:

    def load(
        self,
        file_path: str
    ):

        file = Path(file_path)

        if not file.exists():
            raise FileNotFoundError(
                f"Image not found : {file_path}"
            )

        start = time.time()

        image = cv2.imread(file_path)

        gray = cv2.cvtColor(
            image,
            cv2.COLOR_BGR2GRAY
        )

        text = pytesseract.image_to_string(
            gray
        )

        metadata = {

            "document_id": str(uuid4()),

            "file_name": file.name,

            "file_path": str(file.resolve()),

            "file_type": file.suffix.lower(),

            "file_size": file.stat().st_size,

            "uploaded_at": datetime.utcnow().isoformat(),

            "processing_time": round(
                time.time() - start,
                3
            ),

            "source_type": "doctor_upload",

            "ocr_required": False

        }

        statistics = {

            "character_count": len(text),

            "word_count": len(text.split())

        }

        return {

            "status": "success",

            "text": text,

            "segments": [

                {
                    "index": 1,
                    "type": "ocr_text",
                    "text": text
                }

            ],

            "metadata": metadata,

            "statistics": statistics

        }