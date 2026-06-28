"""
===========================================================
MedShield-X
Dynamic Patient RAG

File:
    document_loader.py

Purpose:
    DocumentLoader — dispatcher that routes a file to the
    appropriate specialised loader based on file extension.

Supported formats:
    ✔ PDF    → PDFLoader
    ✔ DOCX   → DOCXLoader
    ✔ XLSX   → ExcelLoader
    ✔ PNG / JPG / JPEG / BMP / TIFF → ImageLoader
    ✔ TXT / MD → plain-text fallback

Author:
    MedShield-X
===========================================================
"""

from pathlib import Path
from uuid import uuid4
from datetime import datetime

from backend.rag.ingestion.pdf_loader import PDFLoader
from backend.rag.ingestion.docx_loader import DOCXLoader
from backend.rag.ingestion.excel_loader import ExcelLoader
from backend.rag.ingestion.image_loader import ImageLoader


# Map of lowercase file extensions → loader class
_LOADER_MAP = {
    ".pdf":  PDFLoader,
    ".docx": DOCXLoader,
    ".xlsx": ExcelLoader,
    ".xls":  ExcelLoader,
    ".png":  ImageLoader,
    ".jpg":  ImageLoader,
    ".jpeg": ImageLoader,
    ".bmp":  ImageLoader,
    ".tif":  ImageLoader,
    ".tiff": ImageLoader,
}

_PLAIN_TEXT_EXTENSIONS = {".txt", ".md", ".csv"}


class DocumentLoader:
    """
    Routes a file path to the correct specialised loader.
    Returns a normalised document dict with guaranteed keys:
        - status          : str
        - document_text   : str   (full text content)
        - metadata        : dict
        - statistics      : dict
    """

    def load_document(self, file_path: str) -> dict:
        """
        Load a document from *file_path* using the appropriate loader.

        Parameters
        ----------
        file_path : str
            Absolute or relative path to the document.

        Returns
        -------
        dict
            Normalised document dictionary.
        """
        path = Path(file_path)
        ext = path.suffix.lower()

        # ---------- specialised loaders ----------
        loader_cls = _LOADER_MAP.get(ext)
        if loader_cls is not None:
            raw = loader_cls().load(file_path)
            return self._normalise(raw, path, ext)

        # ---------- plain-text fallback ----------
        if ext in _PLAIN_TEXT_EXTENSIONS:
            return self._load_plain_text(path)

        # ---------- unknown format — still try plain text ----------
        try:
            return self._load_plain_text(path)
        except Exception as e:
            raise ValueError(
                f"Unsupported file format '{ext}' and plain-text fallback failed: {e}"
            )

    # ------------------------------------------------------------------
    # Private helpers
    # ------------------------------------------------------------------

    def _normalise(self, raw: dict, path: Path, ext: str) -> dict:
        """
        Ensure the returned dict always exposes both `document_text` and `text`
        regardless of which loader produced it, so every downstream pipeline step
        works correctly (TextCleaner reads `text`, others read `document_text`).
        """
        text = (
            raw.get("document_text")
            or raw.get("text")
            or ""
        )
        raw["document_text"] = text
        raw["text"] = text
        raw.setdefault("metadata", {})
        raw.setdefault("statistics", {})
        return raw

    def _load_plain_text(self, path: Path) -> dict:
        """Minimal plain-text loader used for .txt / .md / unknown files."""
        text = path.read_text(encoding="utf-8", errors="replace")
        return {
            "status": "success",
            "document_text": text,
            "metadata": {
                "document_id": str(uuid4()),
                "file_name": path.name,
                "file_path": str(path.resolve()),
                "file_type": path.suffix.lower(),
                "file_size": path.stat().st_size,
                "uploaded_at": datetime.utcnow().isoformat(),
                "source_type": "doctor_upload",
            },
            "statistics": {
                "character_count": len(text),
                "word_count": len(text.split()),
            },
        }
