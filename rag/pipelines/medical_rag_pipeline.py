from pathlib import Path

from rag.pipelines.pdf_rag_pipeline import (
    PDFRAGPipeline
)


class MedicalRAGPipeline:

    def __init__(self):

        self.pdf_rag = (
            PDFRAGPipeline()
        )

    def index_medical_knowledge(
        self,
        folder_path
    ):

        folder = Path(
            folder_path
        )

        total_chunks = 0

        pdf_files = list(
            folder.glob("*.pdf")
        )

        print(
            f"\nFound {len(pdf_files)} PDFs"
        )

        for pdf_file in pdf_files:

            print(
                f"\nIndexing: {pdf_file}"
            )

            chunks = (
                self.pdf_rag.index_pdf(
                    str(pdf_file),
                    reset_index=False
                )
            )

            print(
                f"Chunks: {chunks}"
            )

            total_chunks += chunks

        print(
            "\n=================================="
        )

        print(
            f"Total Chunks: {total_chunks}"
        )

    def retrieve_context(
        self,
        question,
        top_k=5
    ):

        return (
            self.pdf_rag.query(
                question,
                top_k
            )
        )