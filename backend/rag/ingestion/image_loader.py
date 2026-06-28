"""
===========================================================
MedShield-X

Image Loader

Supports:
    jpg
    jpeg
    png
    bmp
    tif
===========================================================
"""

from pathlib import Path
from uuid import uuid4
from datetime import datetime
import time

from PIL import Image


class ImageLoader:

    def load(self, file_path: str):

        file = Path(file_path)

        if not file.exists():
            raise FileNotFoundError(
                f"Image not found : {file_path}"
            )

        start = time.time()

        image = Image.open(file_path)

        width, height = image.size

        metadata = {

            "document_id": str(uuid4()),

            "file_name": file.name,

            "file_path": str(file.resolve()),

            "file_type": file.suffix.lower(),

            "file_size": file.stat().st_size,

            "image_width": width,

            "image_height": height,

            "image_mode": image.mode,

            "uploaded_at": datetime.utcnow().isoformat(),

            "processing_time": round(
                time.time() - start,
                3
            ),

            "source_type": "doctor_upload",

            "ocr_required": True

        }

        statistics = {

            "width": width,

            "height": height

        }

        image.close()

        return {

            "status": "success",

            "text": "",

            "segments": [],

            "metadata": metadata,

            "statistics": statistics

        }