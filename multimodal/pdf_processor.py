# Placeholder for pdf_processor.py
from pathlib import Path

from pypdf import PdfReader


class PDFProcessor:

    def __init__(self):

        pass

    def extract_text(
        self,
        pdf_path
    ):

        pdf_path = Path(
            pdf_path
        )

        if not pdf_path.exists():

            raise FileNotFoundError(
                f"{pdf_path} not found"
            )

        reader = PdfReader(
            str(pdf_path)
        )

        text = ""

        for page in reader.pages:

            page_text = (
                page.extract_text()
            )

            if page_text:

                text += (
                    page_text + "\n"
                )

        return text

    def get_page_count(
        self,
        pdf_path
    ):

        reader = PdfReader(
            str(pdf_path)
        )

        return len(
            reader.pages
        )