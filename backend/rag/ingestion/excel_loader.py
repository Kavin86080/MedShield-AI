"""
===========================================================
MedShield-X

Excel Loader

Supports:
    .xlsx
    .xls
    .csv
===========================================================
"""

from pathlib import Path
from uuid import uuid4
from datetime import datetime
import time

import pandas as pd


class ExcelLoader:

    def load(self, file_path: str):

        file = Path(file_path)

        if not file.exists():
            raise FileNotFoundError(
                f"Excel file not found : {file_path}"
            )

        start = time.time()

        extension = file.suffix.lower()

        if extension == ".csv":
            df = pd.read_csv(file_path)

        else:
            df = pd.read_excel(file_path)

        rows = []

        for index, row in df.iterrows():

            text = " | ".join(
                [str(value) for value in row.values]
            )

            rows.append(

                {
                    "index": index + 1,
                    "type": "row",
                    "text": text
                }

            )

        document_text = "\n".join(
            row["text"] for row in rows
        )

        metadata = {

            "document_id": str(uuid4()),

            "file_name": file.name,

            "file_path": str(file.resolve()),

            "file_type": extension,

            "file_size": file.stat().st_size,

            "uploaded_at": datetime.utcnow().isoformat(),

            "processing_time": round(
                time.time() - start,
                3
            ),

            "source_type": "doctor_upload"

        }

        statistics = {

            "rows": len(df),

            "columns": len(df.columns),

            "word_count": len(
                document_text.split()
            ),

            "character_count": len(
                document_text
            )

        }

        return {

            "status": "success",

            "text": document_text,

            "segments": rows,

            "metadata": metadata,

            "statistics": statistics

        }